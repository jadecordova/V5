class Tag {

    constructor({
        id = null,
        name = null,
        score = null
    } = {}) {

        this.id = Number(id);
        this.name = name;
        this.score = Number(score);

    }

    Export() {
        return {
            id: this.id,
            name: this.name,
            score: this.score
        };
    }
}