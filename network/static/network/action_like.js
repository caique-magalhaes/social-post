const icon_heart = document.querySelectorAll(".icon-heart")
const icon_heart_filled = document.querySelectorAll(".icon-heart-filled")
const like_number = document.querySelectorAll(".like_number")
const post_id = document.querySelectorAll(".post-id")


//Take each element from the list of heart icons, pay attention to each click, change the image to icon_heart_filled, hide the heart icon, update the number of likes, and retrieve the post, sending it to the sent_like function where you pass the id and the put parameter or delete if you already liked it, to update the Post_likes and Post tables, to keep saving it after a possible page redirection.
icon_heart.forEach((icon,count) =>{
    icon.addEventListener("click", function (e){
        e.preventDefault()
        icon.style.display = "none"
        icon_heart_filled[count].style.display = "block"
        like_number[count].innerHTML = Number(like_number[count].textContent) + 1
        sent_like_post(post_id[count],"PUT")

    })

     icon_heart_filled[count].addEventListener("click", function(e){
            e.preventDefault()
            icon.style.display = "block"
            icon_heart_filled[count].style.display = "none"

            if (Number(like_number[count].textContent) > 0){
                sent_like_post(post_id[count],"DELETE")
                like_number[count].innerHTML = Number(like_number[count].textContent) -1
            }
        })
})

get_like_post()

//Update the database with the posts that the user has already liked and show them to them.
async function get_like_post(){
    const post_id = document.querySelectorAll(".post-id")
    const icon_heart_filled = document.querySelectorAll(".icon-heart-filled")
    const icon_heart = document.querySelectorAll(".icon-heart")

    //gets the posts that the user has already liked
    const response = await fetch("/post/get-like/",{
        method:"GET",
        headers:{
            "X-Requested-With":"XMLHttpRequest",
            "Content-Type":'application/json'
        },
    })

     const show_likes = await response.json()

     
    //Compare the post ID that the user has already liked with the page's post ID to change the heart image to show that a like has been left.
    post_id.forEach((post,count)=>{
        for (let i=0; i <= show_likes.post_like.length; i++){
            if(show_likes.post_like[i] === Number(post.textContent)){
                icon_heart_filled[count].style.display = "block"
                icon_heart[count].style.display = "none"
            }
        }
    })

}


//The function retrieves the ID and the method of the call to determine whether to remove or add a like.
async function sent_like_post(post_id,method_request) {

    console.log(post_id.textContent)
    try{
        const response = await fetch('/post/like',{
            method:method_request,
            body:JSON.stringify({post_id:Number(post_id.textContent)})
        })
        if (response.ok) {
            console.log(response.ok)
        }
        if (!response.ok){
            throw new Error(`Reponse status: ${response.status}`)
        }
    }catch (error){
        console.error(error.message)
    }
}   


