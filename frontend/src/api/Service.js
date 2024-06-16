import axios from "axios"

export default class SendServer{

    //* Функция получения подходящих видео, исходя из текстового запроса
    static async getVideos(searchText){
      return await axios.get(`/api/search?text=${searchText}`)
            .then(response => response.data)
            .catch(error => console.log('Error fetching video: ', error));
    }

    //* Функция автопродления слов и фраз, исходя из текущего текстового запроса
    static async getSuggest(searchText){
      return await axios.get(`/api/search_suggest?text=${searchText}`)
              .then(response => response.data)
              .catch(error => console.log('Error fetching suggest: ', error));
    }

    //* Функция получения кластера тематик
    static async getClusters(){
      return await axios.get('/api/get_clusters')
            .then(response => response)
            .catch(error => console.log('Error fetching clusters: ', error));
    }

    //* Функция получения кластера лиц
    static async getFaces(){
      return await axios.get('/api/get_faces')
            .then(response => response)
            .catch(error => console.log('Error fetching faces: ', error));
    }

    //* Функция получения видео с выбранными лицами
    static async getVideoSelectedFaces(id){
      return await axios.post('/api/get_face_video', {
        'ids': id
      }).then(response => response.data).catch(error => console.log('Error fetching face video: ', error))
    }

    //* Функция получения видео с выбранными тематиками
    static async getVideoSelectedClusters(id){
      return await axios.post('/api/get_cluster_video', {
        'ids': id
      }).then(response => response.data).catch(error => console.log('Error fetching face video: ', error))
    }

    //* Функция получения текста из видео
    static async getTranscription(url){
        try{
            await new Promise(resolve => setTimeout(resolve, 2000)); //! УБРАТЬ ПОЗЖЕ

            const response = "Текст, который мы достали из видео. Внимательно посмотри на ширину текста. Пока текст грузится посередине анимация ожидания. Если текст не распознали, то вместо всего этого будет написано: “Текст из этого видео не распознан”. Если текст очень большой, то появляется ползунок справа.";
            return response;
        } 
        catch (error) {
            console.log("Error fetching transcription: ", error);
        }        
    }

    //* Функция, получения нужной ссылки в yandex cloud 
    static async getLinkYa(){
      return await axios.get('/api/get_upload_url')
        .then(response => response.data)
        .catch(error => console.error('Error fetching upload URL:', error)); 
    }

    //* Загрузка видео в yandex cloud 
    static async putVideo(file, description){
      const ya = await this.getLinkYa();
      const url = ya.url;
      const id = ya.id;           

      try{
        const response = await axios.put(url, file);
        console.log(response);
        if (response.status === 200){
          await this.startProcess(id, description);
        }
        return [response.status, id]
      } 
      catch (error) {
        console.log("Error fetching ya link: ", error);
      }
    }

    //* Загрузка видео ссылки в ya
    static async postVideoLink(url, description){
      try{
        const response = await axios.post("/api/index", {
          'url': url,
          'description': description
        });
        return response;
      } 
      catch (error) {
        console.log(error);
      }
    }

    //* Говорим yandex, что готово можешь делать свои махинации
    static async startProcess(id, description){
      try{
        const response = await axios.post('/api/upload_complete', 
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

