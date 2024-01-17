const rasa = require("rasajs");
rasa.baseUrl("http://localhost:5005");
rasa.sendMessage("hi",res=>{
   console.log(res);
});