class Movie {

    constructor({
        id = null,
        name = null,
        score = null,
        container = null,
        disk = null,
        special = null,
        size = null,
        width = null,
        height = null,
        duration = null,
        codecs = null,
        fps = null,
        extension = null,
        flag = null,
        poster = null,
        filename = null,
        rename = null,
        remove = null,
    } = {}) {

        this.id = Number(id);
        this.name = name;
        this.score = Number(score);
        this.container = container;
        this.disk = disk;
        this.special = special;
        this.size = size;
        this.width = Number(width);
        this.height = Number(height);
        this.duration = duration;
        this.codec = codec;
        this.fps = Number(fps);
        this.extension = extension;
        this.flag = flag;
        this.poster = poster;
        this.filename = filename;
        this.rename = rename;
        this.remove = remove;
    }

    Export() {
        return {
            id: this.id,
            name: this.name,
            score: this.score,
            container: this.container,
            disk: this.disk,
            special: Number(this.special),
            size: this.size,
            width: this.width,
            height: this.height,
            duration: this.duration,
            codec: this.codec,
            fps: this.fps,
            extension: this.extension,
            flag: this.flag,
            poster: this.poster,
            filename: this.filename,
            rename: Number(this.rename),
            remove: Number(this.remove)
        };
    }
}