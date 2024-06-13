import axios from "axios"

export default class SendServer{

    //* Функция получения подходящих видео, исходя из текстового запроса
    static async getVideos(searchText){
        try {
            console.log(searchText);
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

    static async postVideo(file){
      const url = 'https://s3.cloud.ru/my-bucket';
      const fields = {
        'key': '1329',
        'x-amz-algorithm': 'AWS4-HMAC-SHA256',
        'x-amz-credential': '51cc92b6-7a2e-4f81-8d81-ee3fe42a9a93:69c950e74f56bf5498c5d29fa8c62daf/20240613/ru-central-1/s3/aws4_request',
        'x-amz-date': '20240613T112052Z',
        'policy': 'eyJleHBpcmF0aW9uIjogIjIwMjQtMDYtMTNUMTI6MjA6NTJaIiwgImNvbmRpdGlvbnMiOiBbWyJjb250ZW50LWxlbmd0aC1yYW5nZSIsIDAsIDIwMDAwMDAwXSwgeyJidWNrZXQiOiAibXktYnVja2V0In0sIHsia2V5IjogIjEzMjkifSwgeyJ4LWFtei1hbGdvcml0aG0iOiAiQVdTNC1ITUFDLVNIQTI1NiJ9LCB7IngtYW16LWNyZWRlbnRpYWwiOiAiNTFjYzkyYjYtN2EyZS00ZjgxLThkODEtZWUzZmU0MmE5YTkzOjY5Yzk1MGU3NGY1NmJmNTQ5OGM1ZDI5ZmE4YzYyZGFmLzIwMjQwNjEzL3J1LWNlbnRyYWwtMS9zMy9hd3M0X3JlcXVlc3QifSwgeyJ4LWFtei1kYXRlIjogIjIwMjQwNjEzVDExMjA1MloifV19',
        'x-amz-signature': 'd51354f3789404e3b756afb624cbb11e151baef416360026a4db2bfdc339c2ac'
      };

      const formData = new FormData();
      for (const [key, value] of Object.entries(fields)) {
        formData.append(key, value);
      }
      formData.append('file', file);

      // //! отладка
      // for (const [key, value] of formData.entries()) {
      //   console.log(`${key}: ${value}`);
      // }

      try{
        const response = await axios.put(url, formData, 
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log(response.data);
      } 
      catch (error) {
        console.log(error);
      }
    }

}

