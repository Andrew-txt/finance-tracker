from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from src.building_blocks.di import get_current_user_id, Container
from src.operations.application.dto import CreateOperationDTO, CreateTransferDTO, GetOperationStatisticsDTO, OperationDTO, OperationStatisticsDTO
from src.operations.application.operation_service import OperationService

router = APIRouter()


@router.post("/operations", response_model=OperationDTO)
@inject
async def create_operation(operation_data: CreateOperationDTO, operation_service: Annotated[OperationService, Depends(Provide[Container.operation_service])], current_user_id: UUID = Depends(get_current_user_id)):
     return operation_service.create_operation(operation_data=operation_data, user_id=current_user_id)


@router.get("/operations", response_model=OperationStatisticsDTO)
@inject
def get_operations_list(operation_data: GetOperationStatisticsDTO, operation_service: Annotated[OperationService, Depends(Provide[Container.operation_service])], current_user_id: UUID = Depends(get_current_user_id)):
     return operation_service.get_operations_list(statistics_data=operation_data, user_id=current_user_id)


@router.post("/operations/transfer", response_model=OperationDTO)
@inject
def create_transfer(transfer_data: CreateTransferDTO, operation_service: Annotated[OperationService, Depends(Provide[Container.operation_service])], current_user_id: UUID = Depends(get_current_user_id)):
     return operation_service.transfer_between_wallets(transfer_data=transfer_data, user_id=current_user_id)
