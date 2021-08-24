function modifyHTML(NAME, TEMPERATURE, TIMES){
    //html파일에 있는 name공간을 name으로 불러오고, 그 공간에 들어갈 새로운 공간을 생성
    let name = document.getElementsByClassName('name')[0]
    let nameDiv = document.createElement('div')

    //html파일에 있는 temperature공간을 temperature로 불러오고, 그 공간에 들어갈 새로운 공간을 생성
    let temperature = document.getElementsByClassName('temperature')[0]
    let temperatureDiv = document.createElement('div')

    //html파일에 있는 enterLog공간을 enterLog로 불러오고, 그 공간에 들어갈 새로운 공간을 생성
    let enterLog = document.getElementsByClassName('enterLog')[0]
    let enterLogDiv = document.createElement('div')

    //nameDiv, temperatureDiv, enterlogDiv에 들어갈 텍스트 노드를 생성(입력받은 파라미터 값을 여기서 대입시킴)
    let nameText = document.createTextNode(NAME)
    let temperatureText = document.createTextNode(TEMPERATURE)
    let enterLogText = document.createTextNode(TIMES)

    //위에서 만든 텍스트 노드를 각 공간에 맞게 추가
    nameDiv.appendChild(nameText)
    temperatureDiv.appendChild(temperatureText)
    enterLogDiv.appendChild(enterLogText)

    //nameDiv, temperatureDiv, enterlogDiv에 css속성을 입히기 위해 contentBox클래스 추가
    nameDiv.className = "contentBox"
    temperatureDiv.className = "contentBox"
    enterLogDiv.className = "contentBox"

    //최종적으로 html파일에 js를 통해 만든 요소들을 추가시킴
    name.appendChild(nameDiv)
    temperature.appendChild(temperatureDiv)
    enterLog.appendChild(enterLogDiv)
}

$.ajax({
    type:"GET",
    //서버 경로에 있는 Temperature.txt파일을 json형식으로 반환해주는 enterLog api를 이용해서 response에 이를 받아옴
    url:"http://110.165.16.23:1219/enterLog",
    //response에는 {"0": {Temperature 내용}, "1": {Temperature 내용}, "2": {Temperature 내용} ...}
    //위와 같은 형식의 json파일이 넘어와 있으므로(0, 1, 2의 키값에 대응되는 value들은 json형식이 아닌 string형식임) 이를 각 키값으로 구분하여
    //modifyHTML함수의 파라미터 값으로 대입
    success: function(response){
        //for문을 역순으로 돌려서 최근의 출입기록이 가장 위에 찍히도록 함
        for(let i = Object.keys(response).length - 1; i >= 0; i--){
            //큰 따옴표를 기준으로 문자열을 잘라 strings 리스트에 대입
            let strings = response[`${i}`].split('"')
            //strings 리스트에 있는 값들 중 필요한 값들을 찾아내어 필요한 정보만큼을 다시 잘라내어 modifyHTML함수의 파라미터 값으로 대입
            modifyHTML(strings[5], strings[2].slice(2,-3), strings[8].slice(1,-2))
        }
    }
})