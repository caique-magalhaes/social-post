const form_post = document.querySelector('.form_post') 
const title = document.querySelector('#title')


//It retrieves the form, listens for submissions, removes the default update action, and calls the create_post function.
form_post.addEventListener('submit',(e)=>
    {
        e.preventDefault()
        create_post()
    })

    
async function create_post(){
//It retrieves the text description and sends it to the fetch function to update the Post table.
    const description =document.querySelector('#description')


    try{
        const response = await fetch('post/sent',{
            method:'POST',
            body:JSON.stringify({description: description.value})
        })

        //If everything goes well, it will be sent to the index page and you will see your post.
        if (response.ok){
            window.location.href = '/'
        }
        if(!response.ok){
            throw new Error(`Reponse status: ${response.status}`)
        }
    }catch (error){
        console.error(error.message)
    }
}
