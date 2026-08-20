export async function handleTransaction (userLogin, walletName, amount, description, type) {
    try {
        const res = await fetch('/api/v1/operations', {
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
        const res = await fetch('/api/v1/operations/transfer', {
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


export async function fetchUserData(token) {
    if (token != null) {
        const urls = ['/api/v1/users/me', '/api/v1/wallets'];

        const options = {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        }

        try {
            const [resD, resW] = await Promise.all(
                urls.map(async (url) => {
                    const res = await fetch(url, options);
                    
                    if (res.status === 401) {
                        return null;
                    }
                    if (!res.ok) {
                        throw new Error(`Server Error: ${res.status}`);
                    }
                
                    return await res.json();
                })
            );
            
            if ([resD, resW].some(item => item === null)) {
                return null;
            } else {
                return [resD, resW];
            }
        } catch (e) { console.error(e) }

    } else { 
        return null 
    }
    
}

export async function refreshAccessToken(refreshToken) {
    try {
        const res = await fetch('/auth/google/refresh',{
            method: 'POST',
            body: JSON.stringify({
                refresh_token: refreshToken,
            })
        })

        if (!res.ok) {
            throw new Error(`Invalid Refresh Token: ${res.status}`)
        }
        
        const data = await res.json().access_token
        return data.access_token
    } catch (e) {
        return null
    }
}
