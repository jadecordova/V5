class Star {

    constructor({
        id = null,
        name = null,
        score = null,
        movies = null,
        special = null,
        edited = null
    } = {}) {

        this.id = Number(id);
        this.name = name;
        this.score = Number(score);
        this.movies = Number(movies);
        this.special = special;
        this.edited = edited;
    }

    Export() {
        return {
            id: this.id,
            name: this.name,
            score: this.score,
            movies: this.movies,
            special: Number(this.special),
            edited: Number(this.edited)
        };
    }
}