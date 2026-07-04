<template>
  <div>
    <div>



    </div>
   
    <h1>Welcome, {{ this.userName }}!</h1>
    <div class="wallets-holder">
        Your wallets
        <div class="wallet-item" v-for="userWallet in userWallets" :key="userWallet.id">
            <div class="wallet-details">
                <div class="wallet-name">
                    <strong>{{ userWallet.name }}</strong>
                </div>
                <div class="wallet-balance">
                    <span class="balance-amount">{{ formatBalance(userWallet.balance) }}</span>
                    <span class="balance-currency">{{ userWallet.currency.toUpperCase() }}</span>
                </div>
            </div>
            <div class="wallet-operations">
                <button type="button" class="btn-primary" @click="openModal('income', userWallet.name)">
                Добавить доход
                </button>
                <button type="button" class="btn-danger" @click="openModal('expense', userWallet.name)">
                Добавить расход
                </button>
                <button type="button" class="btn-warning" @click="openModal('transfer', userWallet.name)">
                Перевести средства
                </button>
                <TransactionModal
                    v-for="modal in modals"
                    :key="modal.type"
                    :isOpen="modal.isOpen"
                    :type="modal.type"
                    @close="closeModal(modal.type)"
                    @submit="submitForm"
                />
            </div>
        </div>
    </div>


  </div>
</template>

<script>
import { handleTransfer, handleTransaction } from '../utils.js';
import TransactionModal from './TransactionModal.vue';

export default {
    components: {
        TransactionModal
    },
    data() {
        return {
            modals: {
                income: { isOpen: false, type: 'income' },
                expense: { isOpen: false, type: 'expense' },
                transfer: { isOpen: false, type: 'transfer' }
            },
            msg: '',
            userName: '',
     
            userWallets: [],
            login: localStorage.getItem('userLogin'),
            isModalOpen: false

        }
    },
    async mounted() {
        if (this.getUserLogin()) {
            await this.fetchUserData()
            await this.fetchWallets()
    
        }
    },
    methods: {
        openModal(type) {
            this.modals[type].isOpen = true
        },
        closeModal(type) {
            this.modals[type].isOpen = false
        },
        getUserLogin() {
            const userLogin = localStorage.getItem("userLogin")
            if (!userLogin) { this.$router.push('/') }
            return userLogin
        },
        async fetchUserData() {
            const userLogin = this.getUserLogin()
            
            try {
                const res = await fetch('http://127.0.0.1:8000/api/v1/users/me', {
                    method: 'GET',
                    headers: { 
                        'Authorization': `Bearer ${userLogin}`,
                        'Content-Type': 'application/json' 
                    }
                })
                if (res.status === 401) {
                    localStorage.removeItem('userLogin');
                    this.$router.push('/')
                    return
                }
                if (!res.ok) { throw new Error(`Server Error: ${res.status}`) }

                // this.userProfileData = await res.json()
                const data = await res.json()
                this.userName = data.name
                
            } catch (e) {
                console.error(e)
            }
        },
        async fetchWallets() {
            const userLogin = this.getUserLogin()
            
            try {
                const res = await fetch('http://127.0.0.1:8000/api/v1/wallets', {
                    method: 'GET',
                    headers: { 
                        'Authorization': `Bearer ${userLogin}`,
                        'Content-Type': 'application/json' 
                    }
                })
                if (res.status === 401) {
                    localStorage.removeItem('userLogin');
                    this.$router.push('/')
                    return
                }
                if (!res.ok) { throw new Error(`Server Error: ${res.status}`) }

                this.userWallets = await res.json()
            } catch (e) {
                console.error(e)
            }
        },
        formatBalance(value) {
            if (!value) return '0.00'
            const num = parseFloat(value);
            
            if (num < 0.000001 && num > 0) return '< 0.000001'
            return num.toFixed(2);
        },
        async submitForm(transactionData) {
            console.log(transactionData)
            const userLogin = this.getUserLogin()

            if (transactionData.type === 'income') {
                if (await handleTransaction(userLogin, transactionData.walletName, transactionData.amount, transactionData.description, 'income')) {
                    this.msg = "New income added"
                }
            } else if (transactionData.type === 'expense') {
                if (await handleTransaction(userLogin, transactionData.walletName, transactionData.amount, transactionData.description, 'expense')) {
                    this.msg = "New expense added"
                }
            } else if (transactionData.type === 'transfer') {
                if (await handleTransfer(userLogin, transactionData.walletName, transactionData.destinationWalletName, transactionData.amount, transactionData.description)) {
                    this.msg = "New expense added"
                }
            } else {
                this.msg = "Not added"////
            }

        },
    }

}
</script>