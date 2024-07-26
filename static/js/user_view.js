
// alert(moi)
var users = document.getElementsByClassName('view_user')
for (let index = 0; index < users.length; index++) {
    const user_cherche = users[index];
user_cherche.addEventListener('click',function () {
    
    var user_id = this.dataset.id
   
    if (moi=='AnonymousUser') {
           alert('Connectez-vous')
    } else {
        view(user_id)
    }
})
    
}

function view(user) {
    var url = '/view_user'

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type' : 'application/json' ,
            'X-CSRFToken': csrftoken
        } , 

        body:JSON.stringify({
            'user_id' : user
        })
    }).then((response)=>{
        return response.json() ;
    }).then((data)=>{
        console.log('data',data)
    }).catch((error) => {
        console.log('Error:', error);
    });
}