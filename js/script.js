// 当前页码
let currentPage = 1;
// 单页文章size
let itemsPerNums = 3;
// 窗口加载执行方法
window.onload = function () {
    // 隐藏按钮
    hiddenButton();
    // 首次渲染
    displayItems();
    // 隐藏跳转框
    // hiddenPageTurn()
};
// 添加点击事件方法1
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('prev').addEventListener('click', () => changePage(-1));
    document.getElementById('next').addEventListener('click', () => changePage(1));
    // 获取数字输入框
    var pageTurnInput=document.getElementById('pageTurnInput')
    pageTurnInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            console.log(pageTurnInput)
            turnToPage(pageTurnInput.value)
        }
    });
});
// 获取文章数据
const timelines = data["timelines"]
// 计算总页数
let allPage = Math.ceil(timelines.length / itemsPerNums);
// 渲染文章卡片
function displayItems() {
    // 渲染time line
    const contentDiv = document.getElementById('content');
    contentDiv.innerHTML = '';

    const startIndex = (currentPage - 1) * itemsPerNums;
    const endIndex = currentPage * itemsPerNums;
    for (let i = startIndex; i < endIndex && i < timelines.length; i++) {
        // 渲染文章标签
        var tags = timelines[i]["tags"]
        var tagHtml = ''
        for (let j = 0; j < tags.length; j++) {
            tagHtml += `<span class="tag">${tags[j]}</span>`;
        }
        if (timelines[i]["intro"].length > 200) {
            timelines[i]["intro"] = timelines[i]["intro"].substring(0, 200) + '.....';
        }
        // 渲染文章主体
        var timelineHtml = `<div class="timeline">
            <div class="timeline-item">
                <div class="timeline-date">
                    <div class="year-bg">
                        <div class="year">${timelines[i]["year"]}</div>
                    </div>
                    <div class="month-bg">
                        <div class="month">${timelines[i]["month"]}</div>
                    </div>
                </div>
                <div class="timeline-content">
                    <div id="${timelines[i]["id"]}" onclick="turnToArticle('${timelines[i]["href"]}')">
                        <h3>${timelines[i]["title"]}</h3>
                        <p>${timelines[i]["intro"]}</p>
                    </div>
                    <div class="tags">
                        ${tagHtml}
                    </div>
                </div>
            </div>
        </div>`;
        contentDiv.innerHTML += timelineHtml;
    }
}
// 跳转页面
function turnToPage(pageNo) {
    // 取较小值:  取较大值，ceil向上取整
    currentPage = pageNo <= 1 ? Math.max(1, pageNo) : Math.min(pageNo, allPage)
    hiddenButton()
    displayItems();
}
// 上一页、下一页
function changePage(page) {
    currentPage += page;
    turnToPage(currentPage)
}
// 跳转到某篇文章
function turnToArticle(path) {
    window.location.href = path; // 跳转到文章页面
}
// 隐藏翻页按钮
function hiddenButton() {
    var previousPageButton = document.getElementById('prev');
    var nextPageButton = document.getElementById('next');
    // 判断是否是第一页
    if (currentPage == 1) {
        previousPageButton.style.visibility = 'hidden'; // 隐藏上一页按钮
    } else {
        previousPageButton.style.visibility = 'visible'; // 显示上一页按钮
    }
    // 判断是否是最后一页
    if (currentPage == allPage) {
        nextPageButton.style.visibility = 'hidden'; // 隐藏下一页按钮
    } else {
        nextPageButton.style.visibility = 'visible'; // 显示下一页按钮
    }
}
// 隐藏跳转框
// function hiddenPageTurn(){
var pageTurn = document.getElementById('page-turn')
if (allPage < 3) {
    pageTurn.style.visibility = 'hidden';
} else {
    console.log("跳转框")
    pageTurn.innerHTML = `跳转到：第<input type="number" id="pageTurnInput" placeholder="输入页码" min="1" max="${allPage}" class="page-turn-input"></input>页/共${allPage}页`
}
// }