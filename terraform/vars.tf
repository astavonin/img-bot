variable "region" {
  default = "ap-southeast-1"
}

variable "lambda_runtime" {
  default = "python3.6"
}

variable "lambda_memory" {
  default = "512"
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
  default = "/usr/bin/pip3"
}
