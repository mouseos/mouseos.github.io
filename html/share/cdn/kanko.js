console.log("script loaded");
let score=[0,0,0]; 
function add(num){
  score[num-1]=1; console.log(score);
}

function calculateScoreTotal(scoreArray) {
  return scoreArray.reduce((acc, val) => acc + val, 0);
}

function clickElementIfFound() {
  const messageCanvas = document.querySelector('#message_canvas');
  if (messageCanvas && messageCanvas.textContent.includes('ᅟ')) {//ハングル朝鮮語フィラーを入れることで読ませないで判定実現
    const totalScore = calculateScoreTotal(score);
    const elementsToClick = document.querySelectorAll(`#message_canvas a`);

    if (totalScore < elementsToClick.length) {
      elementsToClick[totalScore].click();
    }
  }
}

// MutationObserverのコールバック関数
function mutationCallback(mutationsList, observer) {
  for (const mutation of mutationsList) {
    if (mutation.type === 'childList') {
      clickElementIfFound();
    }
  }
}

// MutationObserverの設定
const observer = new MutationObserver(mutationCallback);

// 監視対象の要素を指定してObserverを開始
const targetNode = document.querySelector('#message_canvas');
const config = { childList: true, subtree: true };
observer.observe(targetNode, config);

// 初回実行
clickElementIfFound();
