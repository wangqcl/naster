$('#btn').on('click',function () {
        const listBtn = document.getElementById('btn');
        const lists = document.getElementById('list-chooses');
        const listsLis = lists.querySelectorAll('li');
        // 列表选项从上而下出现
        let listDown = () => {
            let startHeight = 0;
            let stopHeight = 40;
            let timeId = setInterval(() => {
                startHeight++;
                // 注意：forEach() 方法在 IE8 以下不支持
                listsLis.forEach((item) => {
                    item.style.height = startHeight + 'px';
                });
                if (startHeight >= stopHeight) {
                    clearInterval(timeId);
                }
            }, 10);
            lists.style.display = 'block';
        };
        // 列表选项从下而上消失
        let listUp = () => {
            let startHeight = 40;
            let stopHeight = 0;
            let timeId = setInterval(() => {
                startHeight--;
                listsLis.forEach((item) => {
                    item.style.height = startHeight + 'px';
                });
                if (startHeight <= stopHeight) {
                    clearInterval(timeId);
                }
            }, 10);
            // 这里，如果不延时的话，会直接消失，而没有上拉的效果
            setTimeout(() => {
                lists.style.display = 'none';
            }, 350);
        };

        // 如果列表选项为隐藏，点击则显示；如果列表选项为显示，点击则隐藏
        listBtn.onclick=function(){
            if (lists.style.display == 'none') {
                listDown();
            } else {
                listUp();
            }
        };
});

$('#btn1').on('click',function () {
        const listBtn1 = document.getElementById('btn1');
        const lists1 = document.getElementById('list-chooses1');
        const listsLis1 = lists1.querySelectorAll('li');
        // 列表选项从上而下出现
        let listDown = () => {
            let startHeight = 0;
            let stopHeight = 40;
            let timeId = setInterval(() => {
                startHeight++;
                // 注意：forEach() 方法在 IE8 以下不支持
                listsLis1.forEach((item) => {
                    item.style.height = startHeight + 'px';
                });
                if (startHeight >= stopHeight) {
                    clearInterval(timeId);
                }
            }, 10);
            lists1.style.display = 'block';
        };
        // 列表选项从下而上消失
        let listUp = () => {
            let startHeight = 40;
            let stopHeight = 0;
            let timeId = setInterval(() => {
                startHeight--;
                listsLis1.forEach((item) => {
                    item.style.height = startHeight + 'px';
                });
                if (startHeight <= stopHeight) {
                    clearInterval(timeId);
                }
            }, 10);
            // 这里，如果不延时的话，会直接消失，而没有上拉的效果
            setTimeout(() => {
                lists1.style.display = 'none';
            }, 350);
        };

        // 如果列表选项为隐藏，点击则显示；如果列表选项为显示，点击则隐藏
        listBtn1.onclick=function(){
            if (lists1.style.display == 'none') {
                listDown();
            } else {
                listUp();
            }
        };
});

$('#btn2').on('click',function () {
    const listBtn2 = document.getElementById('btn2');
    const lists2 = document.getElementById('list-chooses2');
    const listsLis2 = lists2.querySelectorAll('li');
    // 列表选项从上而下出现
    let listDown = () => {
        let startHeight = 0;
        let stopHeight = 40;
        let timeId = setInterval(() => {
            startHeight++;
            // 注意：forEach() 方法在 IE8 以下不支持
            listsLis2.forEach((item) => {
                item.style.height = startHeight + 'px';
            });
            if (startHeight >= stopHeight) {
                clearInterval(timeId);
            }
        }, 10);
        lists2.style.display = 'block';
    };
    // 列表选项从下而上消失
    let listUp = () => {
        let startHeight = 40;
        let stopHeight = 0;
        let timeId = setInterval(() => {
            startHeight--;
            listsLis2.forEach((item) => {
                item.style.height = startHeight + 'px';
            });
            if (startHeight <= stopHeight) {
                clearInterval(timeId);
            }
        }, 10);
        // 这里，如果不延时的话，会直接消失，而没有上拉的效果
        setTimeout(() => {
            lists2.style.display = 'none';
        }, 350);
    };

    // 如果列表选项为隐藏，点击则显示；如果列表选项为显示，点击则隐藏
    listBtn2.onclick=function(){
        if (lists2.style.display == 'none') {
            listDown();
        } else {
            listUp();
        }
    };
});

$('#btn3').on('click',function () {
    const listBtn3 = document.getElementById('btn3');
    const lists3 = document.getElementById('list-chooses3');
    const listsLis3 = lists3.querySelectorAll('li');
    // 列表选项从上而下出现
    let listDown = () => {
        let startHeight = 0;
        let stopHeight = 40;
        let timeId = setInterval(() => {
            startHeight++;
            // 注意：forEach() 方法在 IE8 以下不支持
            listsLis3.forEach((item) => {
                item.style.height = startHeight + 'px';
            });
            if (startHeight >= stopHeight) {
                clearInterval(timeId);
            }
        }, 10);
        lists3.style.display = 'block';
    };
    // 列表选项从下而上消失
    let listUp = () => {
        let startHeight = 40;
        let stopHeight = 0;
        let timeId = setInterval(() => {
            startHeight--;
            listsLis3.forEach((item) => {
                item.style.height = startHeight + 'px';
            });
            if (startHeight <= stopHeight) {
                clearInterval(timeId);
            }
        }, 10);
        // 这里，如果不延时的话，会直接消失，而没有上拉的效果
        setTimeout(() => {
            lists3.style.display = 'none';
        }, 350);
    };

    // 如果列表选项为隐藏，点击则显示；如果列表选项为显示，点击则隐藏
    listBtn3.onclick=function(){
        if (lists3.style.display == 'none') {
            listDown();
        } else {
            listUp();
        }
    };
});

$('#btn4').on('click',function () {
    const listBtn4 = document.getElementById('btn4');
    const lists4 = document.getElementById('list-chooses4');
    const listsLis4 = lists4.querySelectorAll('li');
    // 列表选项从上而下出现
    let listDown = () => {
        let startHeight = 0;
        let stopHeight = 40;
        let timeId = setInterval(() => {
            startHeight++;
            // 注意：forEach() 方法在 IE8 以下不支持
            listsLis4.forEach((item) => {
                item.style.height = startHeight + 'px';
            });
            if (startHeight >= stopHeight) {
                clearInterval(timeId);
            }
        }, 10);
        lists4.style.display = 'block';
    };
    // 列表选项从下而上消失
    let listUp = () => {
        let startHeight = 40;
        let stopHeight = 0;
        let timeId = setInterval(() => {
            startHeight--;
            listsLis4.forEach((item) => {
                item.style.height = startHeight + 'px';
            });
            if (startHeight <= stopHeight) {
                clearInterval(timeId);
            }
        }, 10);
        // 这里，如果不延时的话，会直接消失，而没有上拉的效果
        setTimeout(() => {
            lists4.style.display = 'none';
        }, 350);
    };

    // 如果列表选项为隐藏，点击则显示；如果列表选项为显示，点击则隐藏
    listBtn4.onclick=function(){
        if (lists4.style.display == 'none') {
            listDown();
        } else {
            listUp();
        }
    };
});

$('#btn5').on('click',function () {
    const listBtn5 = document.getElementById('btn5');
    const lists5 = document.getElementById('list-chooses5');
    const listsLis5 = lists5.querySelectorAll('li');
    // 列表选项从上而下出现
    let listDown = () => {
        let startHeight = 0;
        let stopHeight = 40;
        let timeId = setInterval(() => {
            startHeight++;
            // 注意：forEach() 方法在 IE8 以下不支持
            listsLis5.forEach((item) => {
                item.style.height = startHeight + 'px';
            });
            if (startHeight >= stopHeight) {
                clearInterval(timeId);
            }
        }, 10);
        lists5.style.display = 'block';
    };
    // 列表选项从下而上消失
    let listUp = () => {
        let startHeight = 40;
        let stopHeight = 0;
        let timeId = setInterval(() => {
            startHeight--;
            listsLis5.forEach((item) => {
                item.style.height = startHeight + 'px';
            });
            if (startHeight <= stopHeight) {
                clearInterval(timeId);
            }
        }, 10);
        // 这里，如果不延时的话，会直接消失，而没有上拉的效果
        setTimeout(() => {
            lists5.style.display = 'none';
        }, 350);
    };

    // 如果列表选项为隐藏，点击则显示；如果列表选项为显示，点击则隐藏
    listBtn5.onclick=function(){
        if (lists5.style.display == 'none') {
            listDown();
        } else {
            listUp();
        }
    };
});

$('#btn6').on('click',function () {
    const listBtn6 = document.getElementById('btn6');
    const lists6 = document.getElementById('list-chooses6');
    const listsLis6 = lists6.querySelectorAll('li');
    // 列表选项从上而下出现
    let listDown = () => {
        let startHeight = 0;
        let stopHeight = 40;
        let timeId = setInterval(() => {
            startHeight++;
            // 注意：forEach() 方法在 IE8 以下不支持
            listsLis6.forEach((item) => {
                item.style.height = startHeight + 'px';
            });
            if (startHeight >= stopHeight) {
                clearInterval(timeId);
            }
        }, 10);
        lists6.style.display = 'block';
    };
    // 列表选项从下而上消失
    let listUp = () => {
        let startHeight = 40;
        let stopHeight = 0;
        let timeId = setInterval(() => {
            startHeight--;
            listsLis6.forEach((item) => {
                item.style.height = startHeight + 'px';
            });
            if (startHeight <= stopHeight) {
                clearInterval(timeId);
            }
        }, 10);
        // 这里，如果不延时的话，会直接消失，而没有上拉的效果
        setTimeout(() => {
            lists6.style.display = 'none';
        }, 350);
    };

    // 如果列表选项为隐藏，点击则显示；如果列表选项为显示，点击则隐藏
    listBtn6.onclick=function(){
        if (lists6.style.display == 'none') {
            listDown();
        } else {
            listUp();
        }
    };
});

$('#btn7').on('click',function () {
    const listBtn7 = document.getElementById('btn7');
    const lists7 = document.getElementById('list-chooses7');
    const listsLis7 = lists7.querySelectorAll('li');
    // 列表选项从上而下出现
    let listDown = () => {
        let startHeight = 0;
        let stopHeight = 40;
        let timeId = setInterval(() => {
            startHeight++;
            // 注意：forEach() 方法在 IE8 以下不支持
            listsLis7.forEach((item) => {
                item.style.height = startHeight + 'px';
            });
            if (startHeight >= stopHeight) {
                clearInterval(timeId);
            }
        }, 10);
        lists7.style.display = 'block';
    };
    // 列表选项从下而上消失
    let listUp = () => {
        let startHeight = 40;
        let stopHeight = 0;
        let timeId = setInterval(() => {
            startHeight--;
            listsLis7.forEach((item) => {
                item.style.height = startHeight + 'px';
            });
            if (startHeight <= stopHeight) {
                clearInterval(timeId);
            }
        }, 10);
        // 这里，如果不延时的话，会直接消失，而没有上拉的效果
        setTimeout(() => {
            lists7.style.display = 'none';
        }, 350);
    };

    // 如果列表选项为隐藏，点击则显示；如果列表选项为显示，点击则隐藏
    listBtn7.onclick=function(){
        if (lists7.style.display == 'none') {
            listDown();
        } else {
            listUp();
        }
    };
});

$('#btn8').on('click',function () {
    const listBtn8 = document.getElementById('btn8');
    const lists8 = document.getElementById('list-chooses8');
    const listsLis8 = lists8.querySelectorAll('li');
    // 列表选项从上而下出现
    let listDown = () => {
        let startHeight = 0;
        let stopHeight = 40;
        let timeId = setInterval(() => {
            startHeight++;
            // 注意：forEach() 方法在 IE8 以下不支持
            listsLis8.forEach((item) => {
                item.style.height = startHeight + 'px';
            });
            if (startHeight >= stopHeight) {
                clearInterval(timeId);
            }
        }, 10);
        lists8.style.display = 'block';
    };
    // 列表选项从下而上消失
    let listUp = () => {
        let startHeight = 40;
        let stopHeight = 0;
        let timeId = setInterval(() => {
            startHeight--;
            listsLis8.forEach((item) => {
                item.style.height = startHeight + 'px';
            });
            if (startHeight <= stopHeight) {
                clearInterval(timeId);
            }
        }, 10);
        // 这里，如果不延时的话，会直接消失，而没有上拉的效果
        setTimeout(() => {
            lists8.style.display = 'none';
        }, 350);
    };

    // 如果列表选项为隐藏，点击则显示；如果列表选项为显示，点击则隐藏
    listBtn8.onclick=function(){
        if (lists8.style.display == 'none') {
            listDown();
        } else {
            listUp();
        }
    };
});