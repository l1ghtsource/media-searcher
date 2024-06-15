import axios from "axios"

export default class SendServer{

    //* Функция получения подходящих видео, исходя из текстового запроса
    static async getVideos(searchText){
        try {
            console.log("Видео по запросу: ", searchText);
            const response = await axios.get(`/api/search?text=${searchText}`)
            console.log(response.data);
            return response.data;
        } 
        catch (error) {
            console.log(error);
        }
    }

    //* Функция получения кластера тематик
    static async getClusters(){
      return await axios.get('/api/get_clusters')
            .then(response => response.data)
            .catch(error => console.log('Error fetching clusters:', error));
    }

    //* Функция получения кластера лиц
    static async getFaces(){
      return await axios.get('/api/get_faces')
            .then(response => response.data)
            .catch(error => console.log('Error fetching faces:', error));
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

    //* Функция, получения нужной ссылки в S3 
    static async getLinkS3(){
      return await axios.get('/api/get_upload_url')
        .then(response => response.data)
        .catch(error => console.error('Error fetching upload URL:', error)); 
    }

    //* Загрузка видео в S3 
    static async putVideo(file, description){
      // const s3 = await this.getLinkS3();
      const url = "https://storage.yandexcloud.net/lct-video-0/0?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=YCAJEHmkOlKYPjr4wENVqB3eX%2F20240615%2Fru-central-1%2Fs3%2Faws4_request&X-Amz-Date=20240615T220301Z&X-Amz-Expires=252000&X-Amz-SignedHeaders=host&X-Amz-Signature=7dc734d271190668890edc40aed3b561da56020f70b9f784805689909a760add";
      // const id = s3.id;           

      try{
        const response = await axios.put(url, file);
        console.log(response.data);
        // if (response.status === 200){
        //   await this.startProcess(0, description);
        // }
      } 
      catch (error) {
        console.log(error);
      }
    }

    //* Загрузка видео ссылки в S3 
    static async postVideoLink(url, description){
      try{
        const response = await axios.post("/api/index", {
          'url': url,
          'description': description
        });
        console.log(response.data);
      } 
      catch (error) {
        console.log(error);
      }
    }

    //* Говорим s3, что готово можешь делать свои махинации
    static async startProcess(id, description){
      try{
        const response = await axios.get('/api/upload_complete', 
          {
            'id': id,
            'description': description
          });
        console.log(response.data);
      } catch (error){
        console.error(error);
      }
    }

}

