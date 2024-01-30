// const async load_task_data = () =>{
//     try {
//         const response = await fetch("http://127.0.0.1:8000/api");
    
//         const result = await response.json();
//         console.log("Success:", result);
//       } catch (error) {
//         console.error("Error:", error);
//       }
    
    
// }

function  load_task_data() {
   fetch("http://127.0.0.1:8000/api")
   .then(res =>res.json())
   .then(data=>console.log(data))
  }

load_task_data()