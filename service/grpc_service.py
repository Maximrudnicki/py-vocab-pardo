import grpc
from auth_pb2 import TokenRequest
from vocab_pb2 import (
    CreateRequest,
    DeleteRequest,
    VocabRequest,
    Empty,
    VocabResponse,
    UpdateRequest,
    UpdateStatusRequest,
    WordRequest,
    ManageTrainingsRequest,
    AddWordToStudentRequest,
    AddWordToStudentResponse,
)
from vocab_pb2_grpc import VocabServiceServicer

from model.word import Word
from service.auth_service import AuthenticationService
from repository.word_repository import WordRepository
from utils.time import convert_to_timestamp


class Vocab(VocabServiceServicer):
    def __init__(self):
        self.word_repository = WordRepository()

    def AddWordToStudent(
        self, request: AddWordToStudentRequest, context
    ) -> AddWordToStudentResponse:
        new_word = Word(
            word=request.word,
            definition=request.definition,
            user_id=request.user_id,
        )
        try:
            word_id = self.word_repository.add(new_word)
        except Exception as e:
            return Empty()

        return AddWordToStudentResponse(word_id=word_id)

    def CreateWord(self, request: CreateRequest, context):
        user_id = AuthenticationService().get_user_id(TokenRequest(token=request.token))
        if user_id is None:
            return Empty()

        new_word = Word(
            word=request.word,
            definition=request.definition,
            user_id=user_id,
        )
        try:
            self.word_repository.save(new_word)
        except Exception as e:
            return Empty()

        return Empty()

    def DeleteWord(self, request: DeleteRequest, context):
        user_id = AuthenticationService().get_user_id(TokenRequest(token=request.token))
        if user_id is None:
            return Empty()

        if self.word_repository.is_owner_of_word(user_id, request.word_id):
            self.word_repository.delete(request.word_id)

        return Empty()

    def UpdateWord(self, request: UpdateRequest, context):
        user_id = AuthenticationService().get_user_id(TokenRequest(token=request.token))
        if user_id is None:
            return Empty()

        updatedWord = Word(
            definition=request.definition,
            user_id=user_id,
        )

        try:
            if self.word_repository.is_owner_of_word(user_id, request.id):
                self.word_repository.update(request.id, updatedWord)
        except Exception as e:
            return Empty()

        return Empty()


    def UpdateWordStatus(self, request: UpdateStatusRequest, context):
        user_id = AuthenticationService().get_user_id(TokenRequest(token=request.token))
        if user_id is None:
            return Empty()
        
        try:
            if self.word_repository.is_owner_of_word(user_id, request.id):
                self.word_repository.update_status(request.id, request.is_learned)
        except Exception as e:
            return Empty()

        return Empty()


    def ManageTrainings(self, request: ManageTrainingsRequest, context):
        user_id = AuthenticationService().get_user_id(TokenRequest(token=request.token))
        if user_id is None:
            return Empty()

        try:
            if self.word_repository.is_owner_of_word(user_id, request.id):
                self.word_repository.manage_trainings(
                    request.id, request.training, request.res
                )
        except Exception as e:
            return Empty()

        return Empty()

    def GetWords(self, request: VocabRequest, context):
        user_id = AuthenticationService().get_user_id(TokenRequest(token=request.token))
        if user_id is None:
            return Empty()

        try:
            words = self.word_repository.find_by_user_id(user_id)
        except Exception as e:
            context.set_details(f"Failed to retrieve words: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return Empty()

        for word in words:
            res = VocabResponse(
                id=word.id,
                word=word.word,
                definition=word.definition,
                createdAt=convert_to_timestamp(word.created_at),
                isLearned=word.is_learned,
                cards=word.cards,
                wordTranslation=word.word_translation,
                constructor=word.constructor,
                wordAudio=word.word_audio,
            )
            yield res

    def FindWord(self, request: WordRequest, context) -> VocabResponse:
        try:
            word = self.word_repository.find_by_id(request.word_id)
        except Exception as e:
            context.set_details(f"Failed to retrieve words: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return Empty()

        return VocabResponse(
            id=word.id,
            word=word.word,
            definition=word.definition,
            createdAt=convert_to_timestamp(word.created_at),
            isLearned=word.is_learned,
            cards=word.cards,
            wordTranslation=word.word_translation,
            constructor=word.constructor,
            wordAudio=word.word_audio,
        )
