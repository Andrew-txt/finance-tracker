from sqlalchemy.orm import Session
from fastapi import APIRouter, Request

from src.building_blocks.di import get_current_user_id, container

from src.wallets.application.dto import CreateWalletDTO, TotalBalanceDTO, UserWalletsDTO, WalletDTO
from src.wallets.application.wallet_service import WalletService
from src.wallets.domain.wallet_repository import IWalletRepository

router = APIRouter()


@router.get("/balance", response_model=TotalBalanceDTO) 
def get_total_balance(request: Request):
    wallet_service = container.wallet_service()
    current_user_id = get_current_user_id(request=request)
    
    return wallet_service.get_total_balance(user_id=current_user_id)


@router.post("/wallets", response_model=WalletDTO)
def create_wallet(request: Request, wallet_data: CreateWalletDTO) -> WalletDTO:
    wallet_service = container.wallet_service()
    current_user_id = get_current_user_id(request=request)
    
    return wallet_service.create(wallet_data=wallet_data, user_id=current_user_id)


@router.get("/wallets", response_model=list[WalletDTO])
def get_all_wallets(request: Request) -> list[WalletDTO]:
    wallet_service = container.wallet_service()
    current_user_id = get_current_user_id(request=request)
    
    return wallet_service.get_all_wallets(user_id=current_user_id)