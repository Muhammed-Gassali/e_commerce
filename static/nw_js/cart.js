var updateBtns = document.getElementsByClassName('update-cart')

for(var i=0; i<updateBtns.length; i++)
{
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        
        console.log("action:",action, "productId:",productId)
        console.log("user:", user)
        if (user === 'AnonymousUser')
        {
            console.log("user not log in")
        }
        else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action)
{
    console.log("user is logined")
    var url = '/updateitem/' 

    fetch (url, {
    method: 'POST',
    headers:{
            'X-CSRFToken':csrftoken,
            'Content-Type':'application/json',  
    },
    body:JSON.stringify({'productId':productId, 'action':action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:',data)
        location.reload()
    })
}
