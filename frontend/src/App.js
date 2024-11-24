import React, { useState, useEffect } from "react";
import VideoCard from "./components/VideoCard";
import ArticleModal from "./components/ArticleModal";

const App = () => {
    // const SERVER = "https://44da-2a09-80c0-192-0-42e5-a7f9-ea72-6968.ngrok-free.app"
    const SERVER = "http://localhost:8005"
    const [appState, setAppState] = useState([
        { id: 1, src: `${SERVER}/output_1.mp4`, content_url: `${SERVER}/article_1.json`, isOpen: false },
        { id: 2, src: `${SERVER}/output_2.mp4`, content_url: `${SERVER}/article_3.json`, isOpen: false },
        { id: 3, src: `${SERVER}/output_3.mp4`, content_url: `${SERVER}/article_4.json`, isOpen: false },
        { id: 4, src: `${SERVER}/output_4.mp4`, content_url: `${SERVER}/article_2.json`, isOpen: false },
    ]);

    const phone_color = "bg-black"

    useEffect(() => {
        const fetchData = async () => {

            // Example requests
            const responses = await Promise.all(appState.map((item) =>
                fetch(item.content_url))
            );

            console.log(responses)


            const data = await Promise.all(responses.map((res) => res.json()));
            setAppState(appState.map((article, index) => {
                article.content = data[index]
                return article
            }));

        };

        fetchData();
        console.log("SIU")
    }, []);


    const handleViewArticle = (articleId) => {
        setAppState(appState.map((article) => {
            if (articleId === article.id) {
                article.isOpen = true;
            }
            return article
        }));
    };

    const handleCloseArticle = (articleId) => {
        setAppState(appState.map((article) => {
            if (articleId === article.id) {
                article.isOpen = false;
            }
            return article
        }));
    };

    return (
        <div className="flex justify-center bg-white h-screen">


            <div class="absolute h-[1250px] w-[650px] mx-auto border-black border-[30px] rounded-[3.6rem] shadow-xl">
                <div class="z-10 w-[186px] h-[28px] bg-black top-0 rounded-b-[1rem] left-1/2 -translate-x-1/2 absolute"></div>
                <div class="h-[46px] w-[10px] bg-black absolute -start-[17px] top-[124px] rounded-s-lg"></div>
                <div class="h-[46px] w-[10px] bg-black absolute -start-[17px] top-[178px] rounded-s-lg"></div>
                <div class="h-[64px] w-[10px] bg-black absolute -end-[17px] top-[142px] rounded-e-lg"></div>
                <div class="rounded-[1.8rem] overflow-hidden bg-white dark:bg-orange-800 h-full">
                    {appState[0].content ? (<div
                        className="h-screen overflow-y-scroll snap-y snap-mandatory"
                    >
                        {appState.map((article) => (<div>
                            <VideoCard
                                key={article.id}
                                videoSrc={article.src}
                                onViewArticle={() => handleViewArticle(article.id)}
                            />
                            <ArticleModal key={article.id + appState.length}
                                isOpen={article.isOpen} onClose={() => handleCloseArticle(article.id)} content={article.content} />
                        </div>
                        ))}
                    </div>) : null}
                </div>
            </div>








        </div >
    );
};

export default App;
