const action_edit = document.querySelectorAll('#action_edit')
const text_post = document.querySelectorAll('.card-text')

//It retrieves a list of `action_edit` buttons (the edit button) and listens for the click event of each one
action_edit.forEach((edit_button, index)=>{
    edit_button.addEventListener("click", function(){
        const parent = edit_button.parentNode
        const wrapped_post = parent.childNodes[1]

        const post_id = wrapped_post.childNodes[1]

        // Once clicked, it locates the clicked button, retrieves the parents of that button, and passes the parent and the text of the post to be edited as parameters (located through the index).
        change_text(parent,text_post[index].textContent)

        //Listen for the click of the save button to call the edit_post function and update the Post table.
        save_edit.addEventListener("click", ()=>{edit_post(post_id,parent)})
    })
})


async function change_text(parent,old_text){
    // With the parent element, we can change the body of the text while keeping the text of the post to be edited in a textarea and display a button to save and send it to the Post table to save.
    parent.innerHTML =  `
                    <div class="card-body">
                        <div class="wrapped-post">
                            <div>
                                <textarea name="" id="change_text" required>${old_text}</textarea>
                            </div>
                        </div>
                        <button type="button" class="btn btn-success" id="save_edit" > Save</button>

                     </div>`
}

 async function edit_post(post_id,parent){
    //It retrieves the parameter, id, and takes the text, changes it, and assigns the value to the variable description, which will be passed to the fetch to update the post table.

    const save_edit = document.querySelector("#save_edit")
    const description =document.querySelector('#change_text')

      try{
          const response = await fetch('/post/edit/',{
              method:'PUT',
              body:JSON.stringify({description: description.value, post_id:post_id.textContent})
          })

          if (response.ok){
              console.log(response.ok)
              const new_values = await response.json()
              
              //The response displays the updated post value and shows the updated text with a success message.
              change_post(new_values,parent)
              
          }
          if(!response.ok){
              throw new Error(`Reponse status: ${response.status}`)
          }
      }catch (error){
          console.error(error.message)
      }
 }

 function change_post(new_value,new_post) {
    //show a success message to the user with new_value
    new_post.innerHTML = `

                <span  class="post-id">${new_value.post_id}</span>
                    <p class="card-text">${new_value.post_description}</p>
                    <div class="alert alert-success" role="alert">
                        Your post has been successfully modified.
                    </div>`
 }
