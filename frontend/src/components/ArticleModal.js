import React from "react";

const ArticleModal = ({ isOpen, onClose, content }) => {
    if (!isOpen) return null;

    return (
        <div className={`absolute border-white rounded-[1.7rem] inset-0 flex bg-white transition-opacity
  ease-in
  duration-700
  ${isOpen ? "opacity-100" : "opacity-0"}`} >

            <div className="justify-center relative flex overflow-scroll">
                <button
                    onClick={onClose}
                    className="fixed ml-[360px] mt-8 bg-red-500 hover:bg-red-600 text-white font-bold  py-1 px-3 rounded-full shadow-md"
                >
                    ×
                </button>
                <div className="m-10 my-24">

                    <div className="">
                        <h1 className="text-4xl font-bold text-black">{content.title}</h1>

                        {content.sections.map((section) => (<div>
                            <h2 className="mt-8 text-2xl">{section.title}</h2>
                            <p className="text-gray-700 mt-3 text-balance">
                                {section.content}
                            </p>
                        </div>))}


                    </div>
                </div>
            </div>
        </div >
    );
};

export default ArticleModal;
