/*!
* Start Bootstrap - Bare v5.0.7 (https://startbootstrap.com/template/bare)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-bare/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
new Chart(document.getElementById("doughnut-chart"), {
    type: 'doughnut',
    data: {
      labels: ["서울", "경기", "대전", "인천", "대구","기타지역"],
      datasets: [
        {
          label: "지역 별 공고 수",
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#F78C6C"],
          data: [986,123,6,6,6,24]
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: '지역 별 공고 수'
      }
    }
});

new Chart(document.getElementById("bar-chart-horizontal"), {
    type: 'horizontalBar',
    data: {
      labels: ["스캐터랩", "브이터치", "뱅크샐러드", "Netmarble", "번개장터","핀다","위대한상상(요기요)","Bagelcode","엠아이큐브솔루션","버즈빌"],
      datasets: [
        {
          label: "Like 상위 10개 회사",
          backgroundColor: ["blue", "orange","green","red","purple","brown","pink","gray","olive","cyan"],
          data: [321,318,268,246,191,178,175,132,127,124]
        }
      ]
    },
    options: {
      legend: { display: false },
      title: {
        display: true,
        text: 'Like 상위 10개 회사'
      }
    }
});