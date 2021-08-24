function modifyHTML(value) {
  //html 코드에 있는 scrollBox element를 가져옴
  let scrollBox = document.getElementsByClassName('scrollBox')[0]

  //사진 이름 생성
  let text = document.createTextNode(value.slice(0,-4))

  //이름 공간, 버튼 공간을 담을 공간 생성
  let div = document.createElement('div')

  //이름, 버튼 공간을 따로 생성(flex로 정렬하기 위해서)
  let nameDiv = document.createElement('div')
  let buttonDiv = document.createElement('div')

  //이름 공간에 이름값 추가
  nameDiv.appendChild(text)

  //버튼 생성
  let button = document.createElement('button')

  //버튼에 '삭제' 텍스트 추가
  button.innerHTML = '삭제'

  //버튼에 사진 이름과 같은 값의 클래스 추가(이후 삭제 기능 구현을 위해서 필요)
  button.className = value.slice(0,-4)

  //버튼에 사진 삭제기능 추가
  button.onclick = function () {
      //사진 이름과 같은 값의 아이디를 가지고 있는 element를 img라는 변수로 불러옴
      let img = document.getElementById(`${this.className}`)
      //버튼이 클릭 되었을때 img로 불러온 element를 삭제하는 기능을 추가함(removeChild를 사용) 대신 얘는 보여지는거만 삭제되는 기능임
      img.parentNode.removeChild(img)
      //서버 경로에 있는 이미지를 삭제하는 api인 /delete를 이용해서 서버 경로의 이미지를 삭제
      $.ajax({
          type:"GET",
          url:`http://110.165.16.23:1219/delete?fileName=${value}`
      })
  }

  //버튼 공간에 앞에서 만든 버튼 추가
  buttonDiv.append(button)

  //flex속성을 사용하기 위해서 이름 공간과 버튼 공간에 클래스 이름 부여
  nameDiv.className = "nameDiv"
  buttonDiv.className = "buttonDiv"

  //위에서 만들었던 공간에 이름 공간과 버튼 공간 추가
  div.appendChild(nameDiv)
  div.appendChild(buttonDiv)

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
  //서버 공간에 있는 사진 이름들을 json형식으로 반환해주는 returnName api를 이용해서 response에 사진 이름들을 담은 json파일을 받음
  url:"http://110.165.16.23:1219/returnName",
  data:{},
  success: function(response){
      for(let i = 0; i < Object.keys(response).length; i++){
          //HTML파일을 수정해주는 modifyHTML함수에 사진이름을 하나씩 보내주어 scrollBox영역을 제어
          modifyHTML(response[`${i}`])
      }
  }
})