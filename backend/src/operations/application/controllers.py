from datetime import datetime
from fastapi import APIRouter, Request
from sqlalchemy.orm import Session

from src.building_blocks.di import get_current_user_id, container
from src.operations.application.dto import CreateOperationDTO, CreateTransferDTO, GetOperationStatisticsDTO, OperationDTO, OperationStatisticsDTO
from src.operations.application.operation_service import OperationService
from src.users.application.user_service import UserService

router = APIRouter()


@router.post("/operations", response_model=OperationDTO)
async def create_operation(request: Request, operation_data: CreateOperationDTO) -> OperationDTO:
     operation_service = container.operation_service()
     current_user_id = get_current_user_id(request)
     
     return operation_service.create_operation(operation_data=operation_data, user_id=current_user_id)


@router.get("/operations", response_model=OperationStatisticsDTO)
def get_operations_list(request: Request, operation_data: GetOperationStatisticsDTO) -> OperationStatisticsDTO:
     operation_service = container.operation_service()
     current_user_id = get_current_user_id(request)

     return operation_service.get_operations_list(statistics_data=operation_data, user_id=current_user_id)


@router.post("/operations/transfer", response_model=OperationDTO)
def create_transfer(request: Request, transfer_data: CreateTransferDTO):
     operation_service = container.operation_service()
     current_user_id = get_current_user_id(request)

     return operation_service.transfer_between_wallets(transfer_data=transfer_data, user_id=current_user_id)
