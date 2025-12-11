document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('partition-btn').addEventListener('click', () => {
        document.getElementById('partition-form').submit();
        document.getElementById('loading-text').hidden = false;
        document.getElementById('partition-btn').disabled = true;
    });
});
