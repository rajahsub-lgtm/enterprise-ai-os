"""
Governed evidence client.

Classification: EAIOS Core

This client packages outputs from the existing governed retrieval seam into
a governed evidence package.

It does not replace the existing governed retrieval seam.
It delegates to an injected governed retrieval client and normalizes its output
for downstream fusion.
"""

from __future__ import annotations

from typing import Any

from src.governance.governed_evidence_package import GovernedEvidencePackage
from src.governance.source_access_request import SourceAccessRequest
from src.governance.source_access_result import SourceAccessResult


class GovernedEvidenceClient:
    def __init__(self, governed_retrieval_client: Any) -> None:
        self.governed_retrieval_client = governed_retrieval_client

    def collect(
        self,
        requests: list[SourceAccessRequest | dict[str, Any]],
    ) -> GovernedEvidencePackage:
        normalized_requests = [
            request
            if isinstance(request, SourceAccessRequest)
            else SourceAccessRequest.from_dict(request)
            for request in requests
        ]

        if not normalized_requests:
            raise ValueError("At least one source access request is required.")

        case_ids = {request.case_id for request in normalized_requests}
        if len(case_ids) != 1:
            raise ValueError("All source access requests must belong to the same case.")

        results: list[SourceAccessResult] = []

        for request in normalized_requests:
            governed_output = self._delegate_to_existing_seam(request)
            results.extend(
                SourceAccessResult.from_governed_output(
                    request,
                    governed_output,
                )
            )

        return GovernedEvidencePackage.from_results(
            case_id=normalized_requests[0].case_id,
            results=results,
        )

    def _delegate_to_existing_seam(
        self,
        request: SourceAccessRequest,
    ) -> dict[str, Any]:
        action_request = request.to_action_request()

        for method_name in [
            "retrieve",
            "search",
            "get",
            "request",
            "execute",
        ]:
            method = getattr(self.governed_retrieval_client, method_name, None)
            if callable(method):
                result = method(action_request)
                if not isinstance(result, dict):
                    raise TypeError(
                        "Existing governed retrieval seam must return a dictionary."
                    )
                return result

        raise TypeError(
            "Injected governed retrieval client must expose one of: "
            "retrieve, search, get, request, execute."
        )
