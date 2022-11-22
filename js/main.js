//with this you can save all data and when you reopen the tracker it will remember it
window.saveDataAcrossSessions = false

var start_record = false
var i = 0
var data_array = []

webgazer.setGazeListener((data, timestamp) => {

    //elapsed time is based on time since begin was called
    
    //it saves the coordinates and the timestamps of the tracking dots until you press again the button "start record"
    if (start_record) {
        var data_obj = new Object()
        data_obj.x = data.x
        data_obj.y = data.y
        data_obj.time = timestamp
        data_array[i] = data_obj
        i++
        setTimeout(100)
    }

}).saveDataAcrossSessions(false)
    .begin()

//it's used to stop the tracker
pause = function () {
    webgazer.pause()
    console.log("Pause")
}

//it's used to resume the tracker
resume = function () {
    webgazer.resume()
    console.log("Resume")
}

var index_image = 0
let img_array = ["griglia", "text", "task", "dv1", "dv2", "dv3", "dv4"]
//it's used to change the background image to the previous one
previous = function () {
    if (index_image > 0) {
        index_image--
        document.getElementById("img").src = "..\\img\\" + img_array[index_image] + ".png"
    }
}

//it's used to change the background image to the next one
next = function () {
    if (index_image < 6) {
        index_image++
        document.getElementById("img").src = "..\\img\\" + img_array[index_image] + ".png"
    }
}

//used to start and stop the acquisition of the data. When it's stopped, the system will save in a csv file all the data gathered before and download it
start = function () {
    start_record = !start_record

    if (start_record)
        document.getElementById("logo").src = "..\\img\\play.png"
    else {
        document.getElementById("logo").src = "..\\img\\pause.png"

        let csvContent = "x,y,timestamp" + "\r\n"
        data_array.forEach((element) => {
            console.log(element)
            let row = element.x + "," + element.y + "," + element.time
            csvContent += row + "\r\n"
        })
        data_array = []

        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csvContent);
        hiddenElement.target = '_blank';

        //provide the name for the CSV file to be downloaded  
        hiddenElement.download = img_array[index_image] + ".csv";
        hiddenElement.click();

        document.getElementById('textInput').value = ''
    }
}