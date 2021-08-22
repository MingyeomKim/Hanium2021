
{/* <script type="text/javascript">
  document.open();
  document.write(`<img src="{{url_for("static",filename="UserImage/${value}")}}" style="width: 100px; height: 100px;">`);
  document.close();
</script> */}

function modifyHTML(value) {
  let scrollBox = document.getElementsByClassName('scrollBox')[0]
  //사진 이름 생성
  let text = document.createTextNode(value.slice(0,-4))
  //이름, 사진, 버튼이 들어갈 공간 생성
  let div = document.createElement('div')

  //스크립트 생성
  // let Script = document.createElement('script')
  // Script.type = 'text/javascript'
  // let scriptText = document.createTextNode()
  // Script.textContent = `document.open();\ndocument.write('<img src="{{url_for("static",filename="UserImage/${value}")}}">')\ndocument.close()`
  //공간에 사진 이름, 스크립트 삽입
  div.appendChild(text)
  // div.appendChild(Script)

  //버튼 생성
  let button = document.createElement('button')
  button.innerHTML = '삭제'
  button.className = value.slice(0,-4)
  //버튼에 사진 삭제기능 추가
  button.onclick = function () {
      let img = document.getElementById(`${this.className}`)
      img.parentNode.removeChild(img)
      $.ajax({
          type:"GET",
          url:`http://110.165.16.23:1219/delete?fileName=${value}`
      })
  }
  
  //공간에 버튼까지 삽입
  div.appendChild(button)

  //공간에 아이디 부여(버튼을 눌러 삭제시 필요한 아이디)
  div.id = value.slice(0,-4)

  //공간에 클래스 이름 부여(css 적용을 위해서 전부 같은 클래스명이 필요함)
  div.className = 'imgContainer'

  //최종적으로 스크롤 박스 안에 이름, 사진, 버튼이 들어있는 공간을 추가시킴
  scrollBox.appendChild(div)
}

//사진의 이름값을 json파일에서 꺼내 순차적으로 modifyHTML함수의 파라미터 값으로 보냄
$.ajax({
  type:"GET",
  url:"http://110.165.16.23:1219/returnName",
  data:{},
  success: function(response){
      for(let i = 0; i < Object.keys(response).length; i++){
          modifyHTML(response[`${i}`])
      }
  }
})