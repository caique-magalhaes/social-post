const following_form = document.querySelector('.following')
const unfollowing_form = document.querySelector('.unfollowing')
const username = document.querySelector('.username').childNodes[1].textContent

//It checks if the +follow button exists; if it does, it reads its click event and activates the follow_function.
if (following_form != null) {
    following_form.addEventListener('submit',(e)=>{
        e.preventDefault()
        follow_function()
    })
}
//The `follow_function` retrieves the username and passes it as a parameter to update the `Following` and `Follower` tables.
async function follow_function(){
    try{
        const response = await fetch('/follow',{
            method:"PUT",
            body:JSON.stringify({following:username})
        })
        if (response.ok) {
            window.location.reload()
        }
        if (!response.ok){
            throw new Error(`Reponse status: ${response.status}`)
        }
    }catch (error){
        console.error(error.message)
    }
}
//It checks if the unfollow button exists; if it does, it reads its click event and activates the unfollow_function.
if (unfollowing_form != null) {

    unfollowing_form.addEventListener('submit',(e)=>{
        e.preventDefault()
        unfollowing_function()
    })
}

//The following function is passed as a delete method and its purpose is to remove the user's following status and update the Following and Follower tables.
async function unfollowing_function(){
    try{
        const response = await fetch('/unfollow',{
            method:"DELETE",
            body:JSON.stringify({unfollowing:username})
        })
        if (response.ok) {
            window.location.reload()
        }
        if (!response.ok){
            throw new Error(`Reponse status: ${response.status}`)
        }
    }catch (error){
        console.error(error.message)
    }
}