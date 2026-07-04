<template>
  <h1>I did it! Log in.</h1>
    <form class="sign-up" @submit.prevent="submitForm">
      <div class="form-group">
        <div class="field">
          <label for="name">Name:</label>
            <input 
              id="name"
              :class="v$.form.userName.$error ? 'is-invalid' : ''"
              v-model.trim="form.userName"
            >
            <p v-if="v$.form.userName.$dirty && v$.form.userName.$invalid" class="invalid-feedback">
              Required three symbols
            </p>
        </div>
        <div class="field">
          <label for="login">Login:</label>
            <input 
              type="text" 
              id="login"
              :class="v$.form.userLogin.$error ? 'is-invalid' : ''"
              v-model.trim="form.userLogin"
            >
            <p v-if="v$.form.userLogin.$dirty && v$.form.userLogin.$invalid" class="invalid-feedback">
              Required five symbols
            </p>
        </div>
      </div>      
      <button type="submit" class="btn btn-primary">Сохранить</button>
    </form>
</template>

<script>
import { useVuelidate } from '@vuelidate/core'
import { required, email, minLength } from '@vuelidate/validators'

export default {
  setup () { 
    const formData = () => this?.form || {}
    return { v$: useVuelidate() } 
  },
  data() {
    return {
      form: {
        userName: '',
        userLogin: ''
      }  
    }
  },
  validations() {
    return {
      form: {
        userLogin: { required, minLength: minLength(5) },
        userName: { required, minLength: minLength(3) }
      }
    }
  },
  methods: {
    async submitForm() {
      this.v$.form.$touch()
      if (this.v$.form.$error) {
        console.log("Validation failed")
      } else {
        console.log("Validation passed")
        try {
            const res = await fetch('http://127.0.0.1:8000/api/v1/users', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: this.form.userName,
                    login: this.form.userLogin
                })
            })
          
            if (!res.ok) {
                throw new Error(`Server Error: ${res.status}`)
            }
          
            const data = await res.json()
            localStorage.setItem("userLogin", data.login)

            this.$router.push(`/profile`)

        } catch (error) {
            console.error(error)
        }
      }
    }
  }
}


</script>


<style> 
.sign-up {
  max-width: 480px;
  margin: 0 auto;
  padding: 40px 35px;
  background: linear-gradient(145deg, #ffffff 0%, #f8faff 100%);
  border-radius: 24px;
  box-shadow: 
    0 20px 60px rgba(67, 97, 238, 0.12),
    0 8px 24px rgba(67, 97, 238, 0.06);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  transition: box-shadow 0.3s ease;
}

.sign-up:hover {
  box-shadow: 
    0 24px 72px rgba(67, 97, 238, 0.18),
    0 8px 28px rgba(67, 97, 238, 0.08);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 22px;
  margin-bottom: 32px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field label {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.3px;
  color: #1a2332;
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: 0.8px;
  color: #5b6f87;
  font-weight: 700;
  margin-left: 4px;
}

.field input {
  padding: 14px 18px;
  font-size: 15px;
  font-family: inherit;
  color: #1a2332;
  background: #ffffff;
  border: 2px solid #e8ecf4;
  border-radius: 14px;
  outline: none;
  transition: all 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
  width: 100%;
  box-sizing: border-box;
}

.field input::placeholder {
  color: #a8b6cc;
  font-weight: 400;
}

.field input:focus {
  border-color: #4361ee;
  box-shadow: 
    0 0 0 4px rgba(67, 97, 238, 0.12),
    0 4px 12px rgba(67, 97, 238, 0.08);
  background: #ffffff;
  transform: translateY(-1px);
}

.field input:hover:not(:focus) {
  border-color: #c8d2e6;
  background: #fcfdff;
}

.field input.is-invalid {
  border-color: #ef476f;
  background: #fff8fa;
  box-shadow: 0 0 0 4px rgba(239, 71, 111, 0.08);
}

.field input.is-invalid:focus {
  border-color: #ef476f;
  box-shadow: 0 0 0 4px rgba(239, 71, 111, 0.15);
}

.invalid-feedback {
  margin: 4px 0 0 4px;
  font-size: 12px;
  font-weight: 500;
  color: #ef476f;
  animation: shakeError 0.4s ease;
}

@keyframes shakeError {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-6px); }
  40% { transform: translateX(6px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(4px); }
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 16px 32px;
  font-size: 15px;
  font-weight: 700;
  font-family: inherit;
  letter-spacing: 0.5px;
  color: #ffffff;
  background: linear-gradient(135deg, #4361ee 0%, #3a56d4 100%);
  border: none;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 0 8px 24px rgba(67, 97, 238, 0.3);
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #3a56d4 0%, #2d4bc4 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(67, 97, 238, 0.35);
}

.btn:hover::before {
  opacity: 1;
}

.btn:active {
  transform: translateY(0px);
  box-shadow: 0 4px 16px rgba(67, 97, 238, 0.25);
}

.btn:focus-visible {
  outline: 3px solid #4361ee;
  outline-offset: 3px;
}

.field input:focus-visible {
  outline: none;
}

.invalid-feedback {
  animation: fadeSlideIn 0.3s ease;
}

@keyframes fadeSlideIn {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 520px) {
  .sign-up {
    padding: 28px 20px;
    border-radius: 18px;
    margin: 0 16px;
  }
  
  .field input {
    padding: 12px 16px;
    font-size: 14px;
  }
  
  .btn {
    padding: 14px 24px;
    font-size: 14px;
  }
}
</style> 