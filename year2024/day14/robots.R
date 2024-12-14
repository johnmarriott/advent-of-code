library(tidyverse)

times <- c(8179)

robots <- read_csv("positions.csv") |> 
  filter(t %in% times)

for (time in times) {
  ggplot(data = robots |> filter(t == time), aes(x=x, y=y)) +
    geom_point() +
    scale_y_reverse() +
    labs(title=glue::glue("{time} s"))
  
  ggsave(glue::glue("plots/{time}.png"))
}