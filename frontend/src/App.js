import React, { useState, useEffect } from "react";
import VideoCard from "./components/VideoCard";
import ArticleModal from "./components/ArticleModal";

const App = () => {
    const [appState, setAppState] = useState([
        { id: 1, src: "http://localhost:8005/output_0.mp4", content_url: "http://localhost:8005/article_1.json", isOpen: false },
        { id: 2, src: "http://localhost:8005/output_0.mp4", content_url: "http://localhost:8005/article_2.json", isOpen: false },
        { id: 3, src: "http://localhost:8005/output_0.mp4", content_url: "http://localhost:8005/article_1.json", isOpen: false },
    ]);

    useEffect(() => {
        const fetchData = async () => {

            // Example requests
            const responses = await Promise.all(appState.map((item) =>
                fetch(item.content_url))
            );


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
        <div className="flex justify-center bg-gray-900 h-screen">
            <div className="mockup-phone border-primary h-full">
                <div className="camera"></div>
                <div className="display">
                    <div
                        className="h-screen overflow-y-scroll snap-y snap-mandatory bg-gray-300"
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
                    </div>
                </div>

            </div>

        </div>
    );
};

export default App;
