function showPre() {
  let pre = document.getElementById("pre")
  pre.className="show"
  let post = document.getElementById("post")
  post.className="hide"
  //console.log('Showing pre-retirement')
}

function showPost() {
  let pre = document.getElementById("pre")
  pre.className="hide"
  let post = document.getElementById("post")
  post.className="show"
  //console.log('Showing post-retirement')
}
