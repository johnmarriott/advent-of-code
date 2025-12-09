library(tidyverse)

read_csv(
  "sample.txt",
  col_names = c("x", "y"),
) |>
  ggplot(aes(x = x, y = y)) +
  geom_polygon(
    fill = "lightgreen", 
    color = "darkred", 
    alpha = 0.7
  ) + 
  labs(title = "Sample input", x = "x", y = "y") +
  theme_minimal()

read_csv(
  "input.txt",
  col_names = c("x", "y"),
) |>
  ggplot(aes(x = x, y = y)) +
  geom_polygon(
    fill = "lightgreen", 
    color = "darkred", 
    alpha = 0.7
  ) + 
  labs(title = "Full input", x = "x", y = "y") +
  theme_minimal()



