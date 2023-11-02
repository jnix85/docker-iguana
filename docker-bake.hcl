variable "TAG" {
    default = "production-28"
}

group "default" {
    targets = [ "iguana" ]
}

target "iguana" {
    output = [ "type=registry" ]
    platforms = [ "linux/amd64", "linux/arm64" ]
    dockerfile = "Dockerfile"
    tags = [ "registry.pupgizmo.com/library/iguana:${TAG}"]
}
