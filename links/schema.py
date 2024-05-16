import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from links.models import Amiibo, Vote
from graphql import GraphQLError

class LinkType(DjangoObjectType):
    class Meta:
        model = Amiibo

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    links = graphene.List(LinkType)
    votes = graphene.List(VoteType)

    def resolve_links(self, info, **kwargs):
        return Amiibo.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

#1
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    name = graphene.String()
    amiiboserie = graphene.String()
    gameseries = graphene.String()
    type = graphene.String()
    posted_by = graphene.Field(UserType)

    #2
    class Arguments:
        url = graphene.String()
        name = graphene.String()
        amiiboserie = graphene.String()
        gameseries = graphene.String()
        type = graphene.String()

    #3
    def mutate(self, info, url, name, amiiboserie, gameseries, type):
        user = info.context.user or None

        link = Amiibo(
            url=url,
            name=name,
            amiiboserie=amiiboserie,
            gameseries=gameseries,
            type=type,
            posted_by=user,
            )
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            name=link.name, 
            amiiboserie=link.amiiboserie,
            gameseries=link.gameseries,
            type=link.type,
            posted_by=link.posted_by,
        )

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            #1
            raise GraphQLError('¡Debes estar registrado para votar!')

        link = Amiibo.objects.filter(id=link_id).first()
        if not link:
            #2
            raise Exception('¡Link invalido!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)

# ...code
# Add the mutation to the Mutation class
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()

