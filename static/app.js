class Boggle {

    constructor() {
        this.words = new Set();
        this.score = 0;
        this.time = 60;

        this.showTimer();
        $('form').on('submit', this.handleSubmit.bind(this));
        this.timer = setInterval(this.countdown.bind(this), 1000);
    }

    async handleSubmit(e) {
        e.preventDefault();

        const guess = $('.guess').val();
        if (!guess) {
            return;
        }
        if (this.words.has(guess)) {
            this.showMessage(`${guess} has already been guessed!`);
            $('.guess').val('');
            return;
        }

        const res = await axios.get('/check', { params: { guess: guess } });
    
        if (res.data.result == 'not-word') {
            this.showMessage(`${guess} is not a word!`);
            $('.guess').val('');
        } else if (res.data.result == 'not-on-board') {
            this.showMessage(`${guess} is not on the game board!`);
            $('.guess').val('');
        } else {
            this.words.add(guess);
            this.score += guess.length;
            this.showScore();
            $('.guess').val('');
        }
    }

    showMessage(text) {
        $('.messages').text(text);
    }

    showScore() {
        $('.score').text(this.score);
    }

    showTimer() {
        $('.timer').text(`${this.time} seconds left.`);
    }

    async countdown() {
        this.time -= 1;
        this.showTimer();

        if (this.time == 0) {
            clearInterval(this.timer);
            $('.guess-form').hide();
            await this.gameOver();
        }
    }

    async gameOver() {
        const res = await axios.post('/game-stats', { score: this.score });

        if (res.data.brokeRecord) {
            this.showMessage(`New record: ${this.score}`);
        } else {
            this.showMessage(`Final Score: ${this.score}`);
        }
    }

}