variable "region" {
  default = "ap-southeast-1"
}

variable "lambda_runtime" {
  default = "python3.6"
}

variable "lambda_memory" {
  default = "256"
}

variable "lambda_timeout" {
  default = 900
}

variable "lambda_payload_filename" {
  default = "lambda.zip"
}

variable "lambda_name" {
  default = "img_bot_lambda"
}

variable "lambda_function_handler" {
  default = "main.lambda_handler"
}

variable "pip_path" {
  default = "~/.local/bin/pip3"
}

variable "user_name" {
  type        = string
  description = "Instagram account user name"
}

variable "password" {
  type        = string
  description = "Instagram account password"
}

variable "hashtags" {
  type        = string
  description = "Comma separated hashtags list"
}
