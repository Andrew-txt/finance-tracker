<template>
  <div v-if="isOpen" class="form-group" @click.self="close">
    <form @submit.prevent="handleSubmit">
      <h2>{{ title }}</h2>
      
      <div class="fieldc">
        <label>{{ amountLabel }}</label>
        <input 
          v-model.number="form.amount" 
          type="number" 
          min="0"
          required
        />
      </div>
      
      <div class="fieldc">
        <label>Enter message</label>
        <input 
          v-model.trim="form.description" 
          type="text" 
        />
      </div>
      
      <!-- Дополнительные поля для конкретных типов -->
      <div v-if="type === 'transfer'" class="fieldc">
        <label>Enter destination wallet name</label>
        <input 
          v-model.trim="form.destinationWalletName" 
          type="text" 
          required
        />
      </div>
      
      <button type="submit">Confirm {{ type }}</button>
      <button type="button" @click="close">Cancel</button>
    </form>
  </div>
</template>

<script>
export default {
  props: {
    isOpen: Boolean,
    type: {
      type: String,
      required: true,
      validator: value => ['income', 'expense', 'transfer'].includes(value)
    },
    walletName: {
      type: String,
      required: true
    },
  },
  emits: ['close', 'submit'],
  data() {
    return {
      form: {
        amount: null,
        description: '',
        destinationWalletName: '',
      }
    }
  },
  computed: {
    title() {
      const titles = {
        income: 'Add Income',
        expense: 'Add Expense',
        transfer: 'Transfer to another wallet'
      }
      return titles[this.type] || 'Transaction'
    },
    amountLabel() {
      const labels = {
        income: 'Income Amount',
        expense: 'Expense Amount',
        transfer: 'Transfer Amount'
      }
      return labels[this.type] || 'Amount'
    }
  },
  methods: {
    handleSubmit() {                  /// вот этот участо смущает, какой то непонятный стек вызовов
      this.$emit('submit', {
        walletName: this.walletName,
        type: this.type,
        ...this.form
      })
      this.resetForm()
      this.close()
    },
    close() {
      this.$emit('close')
      this.resetForm()
    },
    resetForm() {
      this.form = {
        amount: null,
        description: '',
        destinationWalletName: '',
      }
    }
  }
}
</script>