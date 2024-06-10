// import axios from "axios"

export default class SendServer{

    //* Функция получения подходящих видео, исходя из текстового запроса
    static async getVideos(searchText){
        try {
            console.log(searchText);
            // const response = await axios.get(
            //   'https://itut.123581321.ru/api/search_empty',
            //   {
            //     headers: {
            //       'Content-Type': 'application/json',
            //     }
            //   }
            // )

            const response = [
                {
                  url: "https://cdn-st.rutubelist.ru/media/e9/e0/b47a9df14a5e97942715e5e705c0/fhd.mp4",
                  description: "Какая-то инфа, которая была дана + которую мы выявили отдельно",
                  user: "@kto-to_tam",
                  tags: ["#такие_теги", "#ещё_теги", "#и_ещё_теги"],
                }, 
                {
                  url: "https://cdn-st.rutubelist.ru/media/ac/08/3604604b4b8b89e34db1e0e91863/fhd.mp4",
                  description: "Какая-то инфа, которая была дана + которую мы выявили отдельно",
                  user: "@kto-to_tam",
                  tags: ["#такие_теги", "#ещё_теги", "#и_ещё_теги"],
                }, 
                {
                  url: "https://cdn-st.rutubelist.ru/media/bf/6a/f040f0dd4afc90b8eb12c8d76571/fhd.mp4",
                  description: "Какая-то инфа, которая была дана + которую мы выявили отдельно",
                  user: "@kto-to_tam",
                  tags: ["#такие_теги", "#ещё_теги", "#и_ещё_теги"],
                }, 
                {
                  url: "https://cdn-st.rutubelist.ru/media/22/78/acbe27254e819403d46eda7b3171/fhd.mp4",
                  description: "Какая-то инфа, которая была дана + которую мы выявили отдельно",
                  user: "@kto-to_tam",
                  tags: ["#такие_теги", "#ещё_теги", "#и_ещё_теги"],
                },
                {
                  url: "https://cdn-st.rutubelist.ru/media/b9/7a/44c1ef97401abbaaf58511b039c9/fhd.mp4",
                  description: "Какая-то инфа, которая была дана + которую мы выявили отдельно",
                  user: "@kto-to_tam",
                  tags: ["#такие_теги", "#ещё_теги", "#и_ещё_теги"],
                }, 
                {
                  url: "https://cdn-st.rutubelist.ru/media/16/f1/4ba070134b96a979888ba7ce95b7/fhd.mp4",
                  description: "Какая-то инфа, которая была дана + которую мы выявили отдельно",
                  user: "@kto-to_tam",
                  tags: ["#такие_теги", "#ещё_теги", "#и_ещё_теги"],
                },  
              ];
          
            console.log(response);
            return response;
        } 
        catch (error) {
            console.log(error);
        }
    }

    //* Функция получения текста из видео
    static async getTranscription(url){
        try{
            console.log(url);
            await new Promise(resolve => setTimeout(resolve, 2000)); //! УБРАТЬ ПОЗЖЕ

            const response = "Текст, который мы достали из видео. Внимательно посмотри на ширину текста. Пока текст грузится посередине анимация ожидания. Если текст не распознался, то вместо всего этого будет написано: “Текст из этого видео не распознан”. Если текст очень большой, то появляется ползунок справа."
            console.log(response);
            return response;
        } 
        catch (error) {
            console.log(error);
        }        
    }
}

