#!/usr/bin/env python

from kubernetes import client, config
from os import system


def annotate_nginx_ingress(nginx_ingresses):

    #https://github.com/kubernetes-client/python/issues/1880
    patching_command = "kubectl patch ingress {0} -n {1} --type='strategic' --patch-file {2}"
    annotations = "./ingressAnnotations.yaml"

    for nginx_ingress_data in nginx_ingresses:
        ingr, ns = nginx_ingress_data
        system(patching_command.format(ingr, ns, annotations))


def get_nginx_ingresses(networking_api):
    ingress_namespace = "mtest"

    ingresses = networking_api.list_namespaced_ingress(namespace=ingress_namespace)

    nginx_ingresses = []
    for i in ingresses.items:
        nginx_ingress_data = [i.metadata.name, i.metadata.namespace]
        if i.spec.ingress_class_name == "nginx":
            nginx_ingresses.append(nginx_ingress_data)
        elif i.metadata.annotations.get("kubernetes.io/ingress.class") == "nginx":
            nginx_ingresses.append(nginx_ingress_data)

    return nginx_ingresses


def init_config():
    k8s_config = "~/.kube/eksconfig" #FIXME move to main script
    k8s_context = "sso-eks-ahoy-basic"

    config.load_kube_config(config_file=k8s_config, context=k8s_context)
    networking_api = client.NetworkingV1Api()

    return networking_api


def main():
    networking_api = init_config()
    nginx_ingresses = get_nginx_ingresses(networking_api)
    annotate_nginx_ingress(nginx_ingresses)


if __name__ == '__main__': #FIXME
    main()
