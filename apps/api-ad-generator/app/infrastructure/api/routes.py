"""FastAPI ルート定義."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.application.usecases import GenerateAdCopyUseCase
from app.dependencies import get_generate_ad_copy_usecase
from app.domain.entities import AdInput
from app.domain.exceptions import AdGenerationError, InvalidInputError
from app.infrastructure.api.models import (
    AdCopyGenerationRequest,
    AdCopyGenerationResponse,
    ErrorResponse,
    GeneratedAdCopyResponse,
    AdCopyEvaluationResponse,
)


router = APIRouter(tags=["ads"])


@router.post(
    "/generate-ad-copy",
    response_model=AdCopyGenerationResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="広告文を生成する",
    description="商品/サービスの名称、ターゲット層、アピールポイントなどの情報に基づいて、AIが複数の広告文候補とそれぞれの評価を生成します。",
)
async def generate_ad_copy(
    request: AdCopyGenerationRequest,
    usecase: GenerateAdCopyUseCase = Depends(get_generate_ad_copy_usecase),
) -> AdCopyGenerationResponse:
    """広告文を生成するエンドポイント."""
    try:
        # リクエストをドメインエンティティに変換
        ad_input = AdInput(
            product_name=request.product_name,
            target_audience=request.target_audience,
            appeal_points=request.appeal_points,
            tone=request.tone,
            num_copies=request.num_copies,
        )
        
        # ユースケース実行
        ad_copies = await usecase.execute(ad_input)
        
        # レスポンスモデルに変換
        generated_copies: List[GeneratedAdCopyResponse] = []
        for ad_copy in ad_copies:
            evaluation_response = None
            if ad_copy.evaluation:
                evaluation_response = AdCopyEvaluationResponse(
                    relevance_score=ad_copy.evaluation.relevance_score,
                    creativity_score=ad_copy.evaluation.creativity_score,
                    target_audience_appeal=ad_copy.evaluation.target_audience_appeal,
                )
            
            generated_copy = GeneratedAdCopyResponse(
                copy_text=ad_copy.copy_text,
                headline=ad_copy.headline,
                call_to_action=ad_copy.call_to_action,
                evaluation=evaluation_response,
            )
            generated_copies.append(generated_copy)
        
        return AdCopyGenerationResponse(generated_copies=generated_copies)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"message": str(e), "code": "BAD_REQUEST"})
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail={"message": e.message, "code": "BAD_REQUEST"})
    except AdGenerationError as e:
        raise HTTPException(status_code=500, detail={"message": e.message, "code": "INTERNAL_SERVER_ERROR"})
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"message": f"予期しないエラーが発生しました: {str(e)}", "code": "INTERNAL_SERVER_ERROR"}
        )