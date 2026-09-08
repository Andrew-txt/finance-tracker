from decimal import Decimal
from uuid import UUID

from src.building_blocks.errors import BusinessRuleViolationError, RepositoryError
from src.building_blocks.enum import OperationType

from src.operations.application.dto import CreateOperationDTO, CreateTransferDTO, GetOperationStatisticsDTO, OperationDTO, OperationStatisticsDTO
from src.operations.domain.operation_repository import IOperationRepository
from src.operations.domain.operation import Operation, Transfer
from src.wallets.domain.wallet_repository import IWalletRepository
from src.operations.domain.currency_exchanger import IExternalSourceRatesProvider


class OperationService:
    def __init__(self, repository: IOperationRepository, wallet_repository: IWalletRepository, currency_rates_provider: IExternalSourceRatesProvider):
        self.repository = repository
        self.wallet_repository = wallet_repository
        self.currency_rates_provider = currency_rates_provider


    def create_operation(self, operation_data: CreateOperationDTO, user_id: UUID):
        if operation_data.type == OperationType.TRANSFER:
            raise BusinessRuleViolationError("Unallowed operation type")
        
        wallet = self.wallet_repository.get(user_id=user_id, wallet_name=operation_data.wallet_name)
        
        operation = Operation.create(
            wallet_id=wallet.id,
            type=operation_data.type,
            amount=Decimal(operation_data.amount),
            currency=wallet.currency,
            description=operation_data.description
        )
        
        self.repository.save(operation)
        
        if operation_data.type == OperationType.INCOME:   # amount умножается на rate 
            new_balance: Decimal = wallet.balance + Decimal(operation_data.amount) ##### Decimal и int не сходятся. проверить 
            wallet.balance = new_balance
        
        if operation_data.type == OperationType.EXPENSE:
            new_balance: Decimal = wallet.balance - Decimal(operation_data.amount)
            wallet.balance = new_balance
        
        self.wallet_repository.update_balance(balance=new_balance, wallet=wallet)
        
        return OperationDTO(**operation.format())
    

    def transfer_between_wallets(self, transfer_data: CreateTransferDTO, user_id: UUID):
        wallet = self.wallet_repository.get(user_id=user_id, wallet_name=transfer_data.wallet_name)
        destination_wallet = self.wallet_repository.get(user_id=user_id, wallet_name=transfer_data.destination_name)

        transfer = Transfer.create(
            wallet_id=wallet.id,
            amount=transfer_data.amount,
            currency=destination_wallet.currency,
            destination_id=destination_wallet.id,
            description=transfer_data.description
        )
        
        new_balance: Decimal = wallet.balance - Decimal(transfer_data.amount)
        new_destination_balance: Decimal = destination_wallet.balance + Decimal(transfer_data.amount)
        
        self.repository.save(transfer)
        
        self.wallet_repository.update_balance(balance=new_balance, wallet=wallet)
        self.wallet_repository.update_balance(balance=new_destination_balance, wallet=destination_wallet)
        
        return OperationDTO(**transfer.format())


    def get_operations_list(self, statistics_data: GetOperationStatisticsDTO, user_id: UUID):
        if statistics_data.wallet_name:
            wallet = self.wallet_repository.get(user_id=user_id, wallet_name=statistics_data.wallet_name)
        
            if not wallet:
                raise RepositoryError("Wallet not found")
            
            wallets_ids = [wallet.id]
        
        else:
            wallets = self.wallet_repository.get_all_wallets(user_id=user_id)
            wallets_ids = [w.id for w in wallets]

        operations = self.repository.get_list(wallets_ids, statistics_data.date_from, statistics_data.date_to)
        result = []

        for operation in operations:
            result.append(OperationDTO(**operation.format()))

        return OperationStatisticsDTO(
            wallet_name=statistics_data.wallet_name,
            date_from=statistics_data.date_from,
            date_to=statistics_data.date_to,
            operations=result
        )

    def rates_source_healtheck_tmp(self) -> bool: 
        return self.currency_rates_provider.healthcheck()



    


