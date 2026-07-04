export async function handleTransaction (userLogin, walletName, amount, description, type) {
    try {
        const res = await fetch('http://127.0.0.1:8000/api/v1/operations', {
            method: 'POST',
            headers: { 
                'Authorization': `Bearer ${userLogin}`,
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify({
                wallet_name: walletName,
                type: type,
                amount: amount,
                description: description
            })
        })

        if ([200, 201].includes(res.status)) {
            const data = await res.json()
            console.log(data)
            return 1
        } else {
            throw new Error(`Unprocessable response receieved: ${res.status}`)
        }

        return 0
    } catch (e) { console.error(e) }
}
 

export async function handleTransfer(userLogin, walletName, destinationWalletName, amount, description) {
    try {
        const res = await fetch('http://127.0.0.1:8000/api/v1/operations/transfer', {
            method: 'POST',
            headers: { 
                'Authorization': `Bearer ${userLogin}`,
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify({
                wallet_name: walletName,
                destination_name: destinationWalletName,
                amount: amount,
                description: description
            })
        })

        if ([200, 201].includes(res.status)) {
            const data = await res.json()
            console.log(data)
            return 1
        } else {
            throw new Error(`Unprocessable response receieved: ${res.status}`)
        }
        return null
    } catch (e) { console.error(e) }
}