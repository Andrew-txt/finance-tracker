from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import Provide, inject

from src.building_blocks.di import get_current_user_id, Container
from src.wallets.application.dto import CreateWalletDTO, TotalBalanceDTO, UserWalletsDTO, WalletDTO
from src.wallets.application.wallet_service import WalletService

router = APIRouter()


@router.get("/wallets/balance", response_model=TotalBalanceDTO) 
@inject
def get_total_balance(wallet_service: Annotated[WalletService, Depends(Provide[Container.wallet_service])], current_user_id: UUID = Depends(get_current_user_id)):
    return wallet_service.get_total_balance(user_id=current_user_id)


@router.post("/wallets", response_model=WalletDTO)
@inject
def create_wallet(wallet_data: CreateWalletDTO, wallet_service: Annotated[WalletService, Depends(Provide[Container.wallet_service])], current_user_id: UUID = Depends(get_current_user_id)):
    return wallet_service.create(wallet_data=wallet_data, user_id=current_user_id)


@router.get("/wallets", response_model=list[WalletDTO])
@inject
def get_all_wallets(wallet_service: Annotated[WalletService, Depends(Provide[Container.wallet_service])], current_user_id: UUID = Depends(get_current_user_id)):
    return wallet_service.get_all_wallets(user_id=current_user_id)
    