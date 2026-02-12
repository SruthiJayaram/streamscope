CREATE INDEX idx_watch_user ON watch_history(user_id);
CREATE INDEX idx_watch_movie ON watch_history(movie_id);
CREATE INDEX idx_rating_movie ON ratings(movie_id);
