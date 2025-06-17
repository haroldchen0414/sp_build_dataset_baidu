/**
 * 该js文件用于获取百度图片
 * @author: haroldchen0414
 * 仅用于方便获取数据集
 * @param n: 需要获取的图片数量
 */

function createDownload(contents){
    const hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:attachment/text,' + encodeURI(contents);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'baidu_image_urls.txt';
    hiddenElement.click();
}

async function grabImageUrls(n = 50, useOriginalUrl=false){
    const urls = new Set();
    let retryCount = 0;
    const maxRetries = 5;

    console.log(`开始获取百度图片, 目标数量: ${n}`);
    console.log(`使用${useOriginalUrl? '原始地址(data-objurl)': '百度服务器地址(src)'}`);

    function scrollPage(){
        window.scrollBy(0, window.innerHeight);
        console.log('滚动页面加载更多图片...');
    }

    function collectUrls(){
        document.querySelectorAll('img[data-objurl], img.img_7rRSL').forEach(img => {
            const url = useOriginalUrl
            ?img.getAttribute('data-objurl')
            :img.src

            if(url){
                const cleanUrl = url.split('&amp;').join('&').replace(/(\/\/[^/]+\.baidu\.com\/[^?]+).*/, '$1');
                urls.add(cleanUrl);
            }
        });

        return urls.size;
    }

    collectUrls();

    while(urls.size < n && retryCount < maxRetries){
        const before = urls.size;
        scrollPage();
        await new Promise(resolve => setTimeout(resolve, 3000));

        collectUrls();

        if(urls.size === before){
            retryCount++;
            console.log(`未加载新图片，重试次数: ${retryCount}/${maxRetries}`);
        }

        else{
            retryCount = 0;
            console.log(`当前已收集: ${urls.size}/${n}`);
        }
    }

    const result = Array.from(urls).slice(0, n);

    if(result.length > 0){
        console.log(`成功获取 ${result.length} 张图片URL`);
        createDownload(result.join('\n'));

        return result
    }

    else{
        console.log('未找到有效的图片url');
        
        return [];
    }
}

grabImageUrls(100).then(urls => {
    console.log('操作完成', urls)
})