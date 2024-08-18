function copyToClipboard(element) {
    const codeElement = element.previousElementSibling;
    const codeText = codeElement.innerText;
    navigator.clipboard.writeText(codeText).then(() => {
        // 成功复制后更改按钮样式
        element.classList.add('success-icon');
        element.textContent = '';
        element.appendChild(document.createElement('i')).classList.add('fas', 'fa-check');
        // element.classList.add('rotate');

        setTimeout(() => {
            // 一段时间后恢复原样
            element.textContent = '';
            element.appendChild(document.createElement('i')).classList.add('fas', 'fa-copy');
            element.classList.remove('success-icon', 'rotate');
        }, 1000);
    }, () => {
        {
            alert('复制失败，请手动复制代码');
        }
    });
}

// 为每个代码块添加复制按钮
document.querySelectorAll('pre').forEach((preElement) => {
    const button = document.createElement('button');
    button.className = 'copy-button';
    button.textContent = '';
    button.appendChild(document.createElement('i')).classList.add('fas', 'fa-copy');
    button.addEventListener('click', () => {
        copyToClipboard(button);
    });

    // 将按钮放置在 pre 元素的右上角
    preElement.appendChild(button);
});