// const form = document.querySelector(".guessForm");
// const input = document.querySelector("input");
// const result = document.querySelector(".guess_result");
// const score = document.querySelector(".score");
// const timer = document.querySelector(".timer");
// let gameOver = false;

// async function handleSubmit(e) {
//   e.preventDefault();
//   if (gameOver) {
//     return null;
//   }
// res = await axios.post("/guess", { guess: input.value });
// input.value = "";
// response = res.data.result;
// if (res.data.status === "failure") {
//   result.textContent = "Word already guessed!";
// }
// if (response === "ok") {
//   const oldScore = Number(score.textContent);
//   score.textContent = oldScore + res.data.guess.length;
//   result.textContent = "Good Guess!";
// } else if (response === "not-on-board") {
//   result.textContent = "That word is not on the board";
// } else {
//   result.textContent = "That is not a word in our dictionary";
// }
// }
// if (document.querySelector(".guessForm")) {
//   form.addEventListener("submit", handleSubmit);
// }

// const timerInt = setInterval(() => {
//   timer.textContent = Number(timer.textContent) - 1;
//   if (timer.textContent === "0") {
//     gameOver = true;
//     result.textContent = "Game Over!";
//     axios.post("/gameover", { score: score.textContent });
//     clearInterval(timerInt);
//   }
// }, 1000);

class Game {
  constructor() {
    this.form = document.querySelector(".guessForm");
    this.input = document.querySelector("input");
    this.result = document.querySelector(".guess_result");
    this.score = document.querySelector(".score");
    this.timer = document.querySelector(".timer");
    this.gameOver = false;

    if (this.form) {
      this.form.addEventListener("submit", this.handleSubmit.bind(this));
    }

    this.timerInt = setInterval(() => {
      this.decrementTimer();
    }, 1000);
  }

  async handleSubmit(e) {
    e.preventDefault();
    if (this.gameOver) {
      return null;
    }
    const res = await axios.post("/guess", { guess: this.input.value });
    this.input.value = "";
    const response = res.data.result;
    if (res.data.status === "failure") {
      result.textContent = "Word already guessed!";
    }
    if (response === "ok") {
      const oldScore = Number(this.score.textContent);
      this.score.textContent = oldScore + res.data.guess.length;
      this.result.textContent = "Good Guess!";
    } else if (response === "not-on-board") {
      this.result.textContent = "That word is not on the board";
    } else {
      this.result.textContent = "That is not a word in our dictionary";
    }
  }

  decrementTimer() {
    this.timer.textContent = Number(this.timer.textContent) - 1;
    if (this.timer.textContent === "0") {
      this.endGame();
    }
  }

  endGame() {
    this.gameOver = true;
    this.result.textContent = "Game Over!";
    axios.post("/gameover", { score: this.score.textContent });
    clearInterval(this.timerInt);
  }
}

const game = new Game();
