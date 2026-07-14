<template>
    <h1>Welcome, {{ this.userName }}!</h1>
    <div class="wallets-holder">
        <h2>Your Wallets</h2>
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
                    Add income
                </button>
                <button type="button" class="btn-danger" @click="openModal('expense', userWallet.name)">
                    Add expense
                </button>
                <button type="button" class="btn-warning" @click="openModal('transfer', userWallet.name)">
                    Transfer
                </button>
            </div>
        </div>

        <TransactionModal v-if="currentModal.isOpen" :isOpen="currentModal.isOpen" :type="currentModal.type"
            :walletName="currentModal.walletName" @close="closeModal" @submit="submitForm" />
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
            currentModal: {
                isOpen: false,
                type: '',
                walletName: ''
            },
            userName: '',
            userWallets: [],
            msg: '',
        }
    },
    computed: {
        activeModals() {
            return Object.values(this.modals).filter(modal => modal.isOpen)
        }
    },
    async mounted() {
        if (this.getUserLogin()) {
            await this.fetchUserData()
            await this.fetchWallets()
        }
    },
    methods: {
        openModal(type, walletName) {
            this.currentModal = {
                isOpen: true,
                type: type,
                walletName: walletName
            }
            console.log(this.currentModal)
        },
        closeModal(modalId) {
            this.currentModal.isOpen = false
        },
        getUserLogin() {
            const userLogin = localStorage.getItem("userLogin")
            if (!userLogin) { this.$router.push('/') }
            return userLogin
        },
        async fetchUserData() {
            const userLogin = this.getUserLogin()
            try {
                const res = await fetch('/api/v1/users/me', {
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

                const data = await res.json()
                this.userName = data.name
            } catch (e) { console.error(e) }
        },
        async fetchWallets() {
            const userLogin = this.getUserLogin()
            try {
                const res = await fetch('/api/v1/wallets', {
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
            } catch (e) { console.error(e) }
        },
        formatBalance(value) {
            if (!value) return '0.00'
            const num = parseFloat(value);

            if (num < 0.000001 && num > 0) return '< 0.000001'
            return num.toFixed(2);
        },
        async submitForm(transactionData) {
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
                this.msg = "Not added"
            }
        },
    }
}
</script>