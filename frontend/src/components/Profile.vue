<template>
    <h1>Welcome, {{ this.userName }}!</h1>
    <div class="wallets-holder">
        <div v-if="userWallets.length <= 0" class="empty-message">
            You don`t have any wallets
        </div>
        <div class="wallet-item" v-for="userWallet in userWallets" :key="userWallet.id">
            <h2>Your Wallets</h2>
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
import { handleTransfer, handleTransaction, fetchUserData, refreshAccessToken } from '../utils.js';
import TransactionModal from './TransactionModal.vue';

export default {
    components: {
        TransactionModal
    },
    data() {
        return {
            access_token: '',
            refresh_token: '',

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
        if (this.$route.query.code) { 
            const tokens = await this.exchangeCode(this.$route.query.code)
            if (tokens) { 
                localStorage.setItem("refreshToken", tokens.refresh_token)
                localStorage.setItem("accessToken", tokens.access_token)

                this.$router.replace({'query': null});

                await this.fetchUserProfileData(tokens.access_token);
            } else {
                console.log("Couldn`t fetch profile data. Unprocessable response from server.")
            }
        } else {
            const accessToken = localStorage.getItem("accessToken")
            const refreshToken = localStorage.getItem("refreshToken")

            if (accessToken && refreshToken) {
                await this.fetchUserProfileData(accessToken, refreshToken)
            } else {
                const possibleUserLogin = this.getUserLogin()
                if (possibleUserLogin) {

                }

                this.$router.replace('/')
            }
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
            if (!userLogin) { 
                return null
            } 
            return userLogin
        },
        async fetchUserProfileData(accessToken, refreshToken) { 
            const userData = await fetchUserData(accessToken);
            
            if (userData == null) {
                const newAccessToken = await refreshAccessToken(refreshToken)

                if (newAccessToken == null) {
                    this.$router.replace('/');
                    localStorage.removeItem("accessToken")
                    localStorage.removeItem("refreshToken")
                } else {
                    this.access_token = newAccessToken
                }
            } else {
                this.userName = userData[0].name;
                this.userWallets = userData[1];
            }  
        },
        async fetchWallets(token) {
            if (token != null ) {
                try {
                    const res = await fetch('/api/v1/wallets', {
                        method: 'GET',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        }
                    })
                    if (res.status === 401) {
                        this.$router.replace('/')
                    }
                    if (!res.ok) { throw new Error(`Server Error: ${res.status}`) }

                    this.userWallets = await res.json()
                } catch (e) { console.log(e) }
            } else {
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
                        this.$router.replace('/');
                        return
                    }
                    if (!res.ok) { throw new Error(`Server Error: ${res.status}`) }

                    this.userWallets = await res.json()
                } catch (e) { console.error(e) }
            }
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
                    this.msg = 'New income added'
                }
            } else if (transactionData.type === 'expense') {
                if (await handleTransaction(userLogin, transactionData.walletName, transactionData.amount, transactionData.description, 'expense')) {
                    this.msg = 'New expense added'
                }
            } else if (transactionData.type === 'transfer') {
                if (await handleTransfer(userLogin, transactionData.walletName, transactionData.destinationWalletName, transactionData.amount, transactionData.description)) {
                    this.msg = 'New expense added'
                }
            } else {
                this.msg = 'Not added'
            }
        },
        async exchangeCode(code) {
            const url = new URL(`${window.location.origin}/auth/google/tokens/access`);
            url.search = new URLSearchParams({code : code})

            try {
                const res = await fetch(url)
                
                if(res.status === 401) {
                    this.$router.replace('/')
                }
                if(res.ok) {
                    const tokens = await res.json()
                    console.log(tokens)
                
                    localStorage.setItem("refreshToken", tokens.refresh_token)
                    localStorage.setItem("accessToken", tokens.access_token)

                    return tokens
                } else {
                    return null;
                }
            } catch (e) {
                console.log(e)
            }
        }
    }
}
</script>